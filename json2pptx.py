import json, os, re, tempfile, warnings, argparse
from enum import Enum
from pptx import Presentation
from pptx.util import Inches
from PIL import Image
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.lang import MSO_LANGUAGE_ID
from pptx.dml.color import RGBColor
from lxml import etree
from pptx.oxml.xmlchemy import OxmlElement

# 중복 경고는 무시 (선택 사항)
warnings.filterwarnings("ignore", message="Duplicate name:")

pholder = 0

def get_slide_layout_enum(prs):
    """
    주어진 Presentation(prs) 객체에서 slide_layouts의 모든 레이아웃 이름을 순서대로 추출하여,
    각 레이아웃의 인덱스를 값으로 갖는 Python Enum을 생성합니다.

    레이아웃 이름이 유효한 식별자가 아닐 경우, 공백 및 특수문자는 언더바(_)로 변환합니다.

    Args:
        prs (Presentation): python-pptx의 Presentation 객체.

    Returns:
        Enum: 슬라이드 레이아웃 이름과 인덱스를 멤버로 갖는 Enum 클래스.
    """
    layout_members = {}
    for idx, layout in enumerate(prs.slide_layouts):
        # layout.name 속성이 없을 경우에는 기본 이름 사용
        raw_name = getattr(layout, "name", f"LAYOUT_{idx}")
        # 유효한 enum 멤버 이름으로 변환 (대문자로, 숫자로 시작하는 경우 앞에 '_' 추가)
        member_name = re.sub(r"\W|^(?=\d)", "_", raw_name.upper())
        if not member_name:
            member_name = f"LAYOUT_{idx}"
        # 중복 방지를 위해 이미 존재하면 인덱스를 추가
        if member_name in layout_members:
            member_name = f"{member_name}_{idx}"
        layout_members[member_name] = idx
    SlideLayoutEnum = Enum("SlideLayoutEnum", layout_members)
    return SlideLayoutEnum

def clear_slides(prs):
    """
    while 루프를 사용하여 프레젠테이션의 모든 슬라이드를 삭제합니다.
    각 슬라이드에 대해 rId 관계를 삭제한 후, 슬라이드 ID 요소를 제거합니다.
    마지막에 임시 파일로 저장 후 재로드하여 내부 구조를 정리합니다.
    """
    # _sldIdLst는 슬라이드 ID들의 리스트입니다.
    while len(prs.slides._sldIdLst) > 0:
        slide_id = prs.slides._sldIdLst[0]
        # 슬라이드의 관계(rId)를 삭제합니다.
        prs.part.drop_rel(slide_id.rId)
        # 첫 번째 슬라이드를 삭제합니다.
        prs.slides._sldIdLst.remove(slide_id)
    # 내부 구조 정리를 위해 임시 파일에 저장 후 재로드
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
        temp_filename = tmp_file.name
    prs.save(temp_filename)
    new_prs = Presentation(temp_filename)
    os.remove(temp_filename)
    return new_prs

def convert_json_to_pptx(prs, data, layouts):
    """
    TODO: JSON 데이터를 python-pptx를 사용하여 PPTX로 변환하는 로직을 작성하세요.
    아래는 예시로 frontmatter의 title 값을 슬라이드 제목으로 설정하는 간단한 구현입니다.
    """
    for slide in data.get("slides", []):
        layout_name_from_json = slide.get("layout", "title_and_content").upper()
        try:
            layout_index = layouts[layout_name_from_json].value
        except KeyError:
            # 레이아웃 이름이 Enum에 없을 경우 기본 레이아웃 사용
            print(f'Layout "{layout_name_from_json}" not found. Using default layout.')
            layout_index = None
            for layout in layouts:
                if layout.name == "TITLE_AND_CONTENT":
                    layout_index = layout.value
                    break

        slide_layout_idx = prs.slide_layouts[layout_index]
        # print(slide_layout_idx.name)
        current_slide = prs.slides.add_slide(slide_layout_idx)

        p_map = {}
        for i, pl in enumerate(current_slide.placeholders):
            p_map.update({i: slide_layout_idx.placeholders[i].placeholder_format.idx})
        

        # 제목을 설정합니다.
        title = slide.get("title", {"title": { "runs": [{"text": "제목없음."}]}})
        runs = title.get("runs", [])
        if title:
            title_shape = current_slide.shapes.title
            p = title_shape.text_frame.paragraphs[0]
            process_runs(runs, p)

        global pholder_no
        pholder_no = 0
        placeholder_count = len(current_slide.placeholders)
        for pholder_data in slide.get("placeholders", []):
            pholder_no += 1
            if placeholder_count >= pholder_no:
                # print(current_slide.slide_layout.name)
                # print(token)
                try:
                    current_placeholder = current_slide.placeholders[p_map[pholder_no]]
                except Exception as e:
                    pass

                for token in pholder_data:
                    process_token(current_placeholder, token, current_slide)
            else:
                print(f"Error: Placeholder index {pholder_no} exceeds available placeholders.")
            
        # Title placeholder는 무적권 0번이어야 해
        shapes_no_title = [sh for i, sh in enumerate(current_slide.shapes) if i != 0]
        
        shapes = []
        
        for i, shape in enumerate(shapes_no_title):
            if current_slide.shapes.title == shape:
                print(current_slide.shapes.title.text_frame.text)
                continue
            placeholder = current_slide.slide_layout.placeholders[i+1]
            shapes.append(dict_shape(shape, placeholder))

        # Shape의 size는 한 번에 대입해줘야 한다. 하나씩 변경하면 0으로 초기화됨
        for i,shape in enumerate(shapes_no_title):
            grow = shapes[i].get("grow", False)
            if grow:
                foo_shp = dict_shape(shape)
                l, r, a, b = expand(shapes, i, prs).values()
                if grow in [1,2,3]:
                    foo_shp['height'] += b
                if grow in [1,4,7]:
                    foo_shp['left'] -= l
                    foo_shp['width'] += l + r
                if grow in [3,6,9]:
                    foo_shp['width'] += r
                if grow in [7,8,9]:
                    foo_shp['top'] -= a
                    foo_shp['height'] += a + b
                if grow == 5:
                    foo_shp['left'] -= l
                    foo_shp['top'] -= a
                    foo_shp['width'] += l + r
                    foo_shp['height'] += a + b
                # 한꺼번에 지정해야한다. 지정할 때 나머지가 0으로 초기화되기 때문. left/top이 width/height와 세트인 것으로 보임.
                shape.left = foo_shp['left']
                shape.top = foo_shp['top']
                shape.width = foo_shp['width']
                shape.height = foo_shp['height']

def calc_resloc(p, i, align=5):
    """
    Placeholder와 이미지 객체를 사용하여 이미지의 위치와 크기를 계산합니다.
    이미지가 placeholder 내에서 align 매개변수에 따라 정렬되도록 위치를 조정합니다.

    인자:
      p: placeholder 객체로, p.left, p.top, p.width, p.height 속성을 가짐.
      i: 이미지 객체로, i.size가 (width, height) 튜플을 제공함.
      align: 이미지 정렬 값 (1~9, numpad 비유). 기본값은 5 (가운데).
             만약 1-9 범위의 정수가 아니면 기본값 5가 사용됩니다.
             numpad 정렬 매핑:
               7: 왼쪽 위,   8: 가운데 위,  9: 오른쪽 위,
               4: 왼쪽 중간, 5: 가운데,      6: 오른쪽 중간,
               1: 왼쪽 아래, 2: 가운데 아래, 3: 오른쪽 아래.

    반환:
      resloc: 이미지의 최종 좌표와 크기를 담은 dict (left, top, width, height)
    """
    # align 값을 정수로 변환 시도, 실패하거나 1~9 범위가 아니면 기본값 5 사용
    
    try:
        align_val = int(align)
    except Exception:
        align_val = 5
    if align_val < 1 or align_val > 9:
        align_val = 5

    # numpad 정렬 값에 따른 가로 정렬 계수: 왼쪽=0, 가운데=0.5, 오른쪽=1
    if align_val in (1, 4, 7):
        factor_x = 0
    elif align_val in (2, 5, 8):
        factor_x = 0.5
    else:  # align_val in (3, 6, 9)
        factor_x = 1

    # numpad 정렬 값에 따른 세로 정렬 계수: 위=0, 가운데=0.5, 아래=1
    if align_val in (7, 8, 9):
        factor_y = 0
    elif align_val in (4, 5, 6):
        factor_y = 0.5
    else:  # align_val in (1, 2, 3)
        factor_y = 1

    # Placeholder의 좌표와 크기
    p_left = p.left
    p_top = p.top
    p_width = p.width
    p_height = p.height
    p_ratio = p_width / p_height

    # 이미지의 원본 크기 및 비율
    i_width, i_height = i.size
    i_ratio = i_width / i_height

    if i_ratio < p_ratio:
        # 이미지가 placeholder보다 상대적으로 좁은 경우: 높이를 맞추고 너비를 조절
        new_width = p_height * i_ratio
        # 남는 가로 공간을 factor_x에 따라 오프셋 적용
        new_left = p_left + (p_width - new_width) * factor_x
        resloc = {
            "left": new_left,
            "top": p_top,  # 세로는 꽉 채움
            "width": new_width,
            "height": p_height,
        }
    else:
        # 이미지가 placeholder보다 상대적으로 넓은 경우: 너비를 맞추고 높이를 조절
        new_height = p_width / i_ratio
        # 남는 세로 공간을 factor_y에 따라 오프셋 적용
        new_top = p_top + (p_height - new_height) * factor_y
        resloc = {
            "left": p_left,  # 가로는 꽉 채움
            "top": new_top,
            "width": p_width,
            "height": new_height,
        }
    return resloc

def unbullet(p):
    p._pPr.insert(
        0,
        etree.Element(
            "{http://schemas.openxmlformats.org/drawingml/2006/main}buNone"
        ),
    )
    p._element.get_or_add_pPr().set("marL", "0")
    p._element.get_or_add_pPr().set("indent", "0")

def titlify(p):
    """
    주어진 paragraph(p)에 대해 major theme fonts를 명시적으로 설정.
    - Latin: +mj-lt
    - East Asian: +mj-ea
    """
    # <a:defRPr> 요소 생성 또는 가져오기
    pPr = p._element.get_or_add_pPr()
    defRPr = pPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}defRPr")
    if defRPr is not None:
        # 기존 거 있으면 제거 (덮어쓰기 위해)
        pPr.remove(defRPr)

    defRPr = OxmlElement("a:defRPr")

    # <a:latin typeface="+mj-lt"/>
    latin = OxmlElement("a:latin")
    latin.set("typeface", "+mj-lt")

    # <a:ea typeface="+mj-ea"/>
    ea = OxmlElement("a:ea")
    ea.set("typeface", "+mj-ea")

    defRPr.append(latin)
    defRPr.append(ea)

    # defRPr 추가
    pPr.append(defRPr)

def process_token(current_placeholder, token, current_slide):

    match(token.get("type", "")):
        case "paragraph":
            p = define_paragraph(current_placeholder)
            unbullet(p)
            process_runs(token.get("runs", []), p)
        case "heading":
            p = define_paragraph(current_placeholder)
            # unbullet(p)
            # titlify(p)
            # p.font.color.theme_color = MSO_THEME_COLOR.ACCENT_2
            # p.level = token.get("depth", 0)
            match(token.get("level", 3)):
                case 3:
                    p.level = 8
                case _:
                    p.level = 7
            process_runs(token.get("runs", []), p)
        case "block_quote":
            p = define_paragraph(current_placeholder)
            p.level = 6
            process_runs(token.get("runs", []), p)
        case "code":
            p = define_paragraph(current_placeholder)
            p.level = 5
            p.text = token.get("lang","code")+'\n\n'+ token.get("raw", "")
        case "image":
            url = token.get("url", "")
            
            try:
                i = Image.open(url)
                            
                global pholder_no
                
                dynloc = {"order": pholder_no}

                try:
                    align_dict = json.loads(current_slide.slide_layout.placeholders[pholder_no].name)
                    dynloc.update(align_dict)
                except:
                    # print('Error: Placeholder name is not JSON format.')
                    pass
                
                resloc = calc_resloc(current_placeholder, i, dynloc.get("align",5))

                try:
                    current_placeholder.insert_picture(url)
                except Exception as e:

                    sp = current_placeholder._element
                    sp.getparent().remove(sp)

                    current_slide.shapes.add_picture(url, **resloc)
            except:
                print(f"Error: Image '{url}' not found or invalid.")

        case "list":
            children = token.get("children", [])
            if children:
                for child in children:
                    p = define_paragraph(current_placeholder)
                    # print(child.get("type", ""))
                    p.level = child.get("depth", 0)
                    process_runs(child.get("runs", []), p)
                    if child.get("ordered", False):
                        orderify(p)

        case _ :
            # print(token.get("type", ""))
            pass

def orderify(p):
    """
    p.level 값을 기준으로 번호 스타일 설정
    """
    level = p.level

    # 원하는 스타일 매핑
    # 참고: https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.autonumberschemevalues
    style_map = {
        0: "romanUcPeriod",  # I.
        1: "arabicPeriod",   # 1.
        2: "alphaLcParenR",  # a)
        3: "alphaUcParenR",  # A)
        4: "romanLcParenR",  # i)
    }

    auto_num_type = style_map.get(level, "arabicPeriod")

    pPr = p._element.get_or_add_pPr()

    # 기존 불릿 제거
    for tag in ["a:buChar", "a:buAutoNum"]:
        el = pPr.find(f".//{tag}", namespaces={"a": "http://schemas.openxmlformats.org/drawingml/2006/main"})
        if el is not None:
            pPr.remove(el)

    # buAutoNum 추가
    buAutoNum = OxmlElement("a:buAutoNum")
    buAutoNum.set("type", auto_num_type)
    pPr.append(buAutoNum)

def define_paragraph(placeholder):
    """
    Placeholder에서 첫 번째 단락을 가져오고, 텍스트가 비어있으면 새 단락을 추가합니다.
    """
    if placeholder.text_frame.paragraphs[0].text != "":
        paragraph = placeholder.text_frame.add_paragraph()
    else:
        paragraph = placeholder.text_frame.paragraphs[0]
    return paragraph

def set_highlight(run, color):
    # get run properties
    rPr = run._r.get_or_add_rPr()
    # Create highlight element
    hl = OxmlElement("a:highlight")
    # Create specify RGB Colour element with color specified
    srgbClr = OxmlElement("a:srgbClr")
    setattr(srgbClr, "val", color)
    # Add colour specification to highlight element
    hl.append(srgbClr)
    # Add highlight element to run properties
    setattr(rPr, "lang", MSO_LANGUAGE_ID.ENGLISH_US)
    setattr(rPr, "altLang", MSO_LANGUAGE_ID.KOREAN)
    # lang="en-US" altLang="ko-KR"
    rPr.append(hl)
    latin = OxmlElement("a:latin")
    # <a:latin typeface="Consolas" panose="020B0609020204030204" pitchFamily="49" charset="0"/>
    setattr(latin, "typeface", "Consolas")
    setattr(latin, "charset", "0")
    rPr.append(latin)
    return run

def process_runs(runs, paragraph):
    """
    주어진 runs 리스트를 사용하여 paragraph에 텍스트와 스타일을 설정합니다.
    각 run은 텍스트와 스타일 정보를 포함하는 딕셔너리입니다.
    """
    for run in runs:
        r = paragraph.add_run()
        r.text = run.get("text", "")
        font = r.font
        if 'bold' in run:
            font.bold = True
            font.color.theme_color = MSO_THEME_COLOR.ACCENT_3
        if 'italic' in run:
            font.italic = True
            font.underline = True
        if 'monospace' in run:
            r = set_highlight(r, 'EEEEEE')
            r.font.color.theme_color = MSO_THEME_COLOR.ACCENT_2
            # r.font.color.rgb = RGBColor(248, 104, 107)
            # print(font.size)
            # 현재 폰트 사이즈를 알아내는 게 쉽지 않다.
        if 'hyperlink' in run:
            r.hyperlink.address = run.get("hyperlink", "https://google.com")

def add_title_slide(prs, frontmatter):
    """
    주어진 Presentation 객체(prs)에 제목 슬라이드를 추가합니다.
    frontmatter는 제목 슬라이드에 표시할 정보를 포함하는 딕셔너리입니다.
    """
    title_slide_layout = prs.slide_layouts[0]  # 제목 슬라이드 레이아웃
    slide = prs.slides.add_slide(title_slide_layout)
    pp = prs.core_properties

    # 이후 placeholder 이름과 md-frontmatter key를 매치할 것
    title = frontmatter.get("title", False)
    subtitle = frontmatter.get("subtitle", False)
    author = frontmatter.get("author", False)   
    
    slide.shapes.title.text = title if title else "제목없음"
    pp.title = title if title else "Powerpoint 프레젠테이션"
    
    if subtitle:
        first_slide_subtitle = slide.placeholders[1]
        first_slide_subtitle = subtitle
        pp.subtitle = subtitle
    if author:
        pp.author = author

def expand(shapes, idx, p):

    def coordinatify(shape):
        return {
            **shape,
            "right": shape["left"] + shape["width"],
            "bottom": shape["top"] + shape["height"],
            "tl": (shape["top"], shape["left"]),
            "tr": (shape["top"], shape["left"] + shape["width"]),
            "bl": (shape["top"] + shape["height"], shape["left"]),
            "br": (shape["top"] + shape["height"], shape["left"] + shape["width"]),
        }

    def are_related(foo, bar, direction):
        if direction == "left":
            # bar가 foo의 왼쪽에 있고, 세로(y축) 범위가 겹치는지
            return bar["left"] + bar["width"] <= foo["left"] and \
                max(foo["top"], bar["top"]) <= min(foo["top"] + foo["height"], bar["top"] + bar["height"])

        elif direction == "right":
            # bar가 foo의 오른쪽에 있고, 세로(y축) 범위가 겹치는지
            return bar["left"] >= foo["left"] + foo["width"] and \
                max(foo["top"], bar["top"]) <= min(foo["top"] + foo["height"], bar["top"] + bar["height"])

        elif direction == "above":
            # bar가 foo의 위에 있고, 가로(x축) 범위가 겹치는지
            return bar["top"] + bar["height"] <= foo["top"] and \
                max(foo["left"], bar["left"]) <= min(foo["left"] + foo["width"], bar["left"] + bar["width"])

        elif direction == "below":
            # bar가 foo의 아래에 있고, 가로(x축) 범위가 겹치는지
            return bar["top"] >= foo["top"] + foo["height"] and \
                max(foo["left"], bar["left"]) <= min(foo["left"] + foo["width"], bar["left"] + bar["width"])

    def find_canvas(shapes):
        top = min([shape["top"] for shape in shapes])
        left = min([shape["left"] for shape in shapes])
        width = max([shape["left"] + shape["width"] for shape in shapes]) - left
        height = max([shape["top"] + shape["height"] for shape in shapes]) - top
        s = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
        }
        return coordinatify(s)
    
    def greater_margin(foo, bar):
        def emu(val):
            return int(val * 914400)
        f = foo.get("margin",0)
        b = bar.get("margin",0)
        return emu(f) if  f > b else emu(b)
    
    canvas = find_canvas(shapes)
    sphs = [coordinatify(shape) for shape in shapes]
    dir = {
        "d" : ("left", "right", "above", "below"),
        "left": ("left", "right"),
        "right": ("right", "left"),
        "above": ("top", "bottom"),
        "below": ("bottom", "top")
    }
    
    foo = sphs.pop(idx)
    bars = sphs
    
    deltas = {
        'left' : 0,
        'right' : 0,
        'above' : 0,
        'below' : 0,
    }
    
    for d in dir['d']:
        related = [s for s in bars if are_related(foo, s, d)]
        if bool(related):
            most_close = min(abs(foo[dir[d][0]]-bar[dir[d][1]]) - greater_margin(foo,bar) for bar in related)
            deltas.update({d: most_close})
        else:
            reaching_canvas = abs(foo[dir[d][0]]-canvas[dir[d][0]])
            deltas.update({d: reaching_canvas})

    return deltas

def dict_shape(shape, placeholder=None):
    """
    주어진 shape 객체의 속성을 딕셔너리 형태로 반환합니다.
    """
    try: 
        from_pl = json.loads(placeholder.name)
    except:
        from_pl = {}
    return {
        "name": shape.name,
        "top": shape.top,
        "left": shape.left,
        "width": shape.width,
        "height": shape.height,
        **from_pl,
    }

def main(data=None):
    parser = argparse.ArgumentParser(
        description="Convert JSON to PPTX using python-pptx"
    )
    parser.add_argument(
        "-r",
        "--ref",
        type=str,
        default=None,
        help="Reference PPTX file path (if provided and non-empty, slides will be cleared)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.pptx",
        help="Output PPTX file name (default: output.pptx)",
    )
    parser.add_argument(
        "-i", "--input", type=str, default=None, help="Input JSON file path"
    )
    parser.add_argument(
        "--return-pptx", action="store_true", help="Return Presentation object instead of saving to file"
    )
    args = parser.parse_args()

    # 환경 변수에서 매개변수 가져오기
    ref_from_env = os.environ.get("JSON2PPTX_REF", "")
    output_from_env = os.environ.get("JSON2PPTX_OUTPUT", "")
    return_pptx_from_env = os.environ.get("JSON2PPTX_RETURN_PPTX", "")

    # 환경 변수에서 가져온 값으로 args 업데이트
    if ref_from_env and not args.ref:
        args.ref = ref_from_env
    if output_from_env and not args.output:
        args.output = output_from_env
    if return_pptx_from_env and not args.return_pptx:
        args.return_pptx = True

    # JSON 데이터 로딩: 딕셔너리를 직접 전달받은 경우 우선 사용
    if data is None:
        if args.input is None:
            print(
                "Error: Please provide input JSON file path with -i/--input option or pass a dictionary to main()."
            )
            return
        else:
            if not os.path.exists(args.input):
                print(f"Error: JSON file '{args.input}' does not exist.")
                return
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)

    # 참조 PPTX 파일이 지정되었고 존재하면 이를 사용합니다.
    if args.ref and os.path.exists(args.ref):
        prs = Presentation(args.ref)
        # 슬라이드가 있다면 완전히 제거 (첫 슬라이드도 포함)
        if len(prs.slides) > 0:
            prs = clear_slides(prs)
    else:
        # 참조 파일이 없으면 새 프레젠테이션 생성
        prs = Presentation()
        
    add_title_slide(prs, data['frontmatter'])

    layouts = get_slide_layout_enum(prs)
    # for layout in layouts:
    #     print(f"{layout.name} = {layout.value}")

    # JSON 데이터를 기반으로 PPTX 변환 로직 실행 (개발자가 직접 구현)
    convert_json_to_pptx(prs, data, layouts=layouts)

    # Presentation 객체 반환 모드
    if args.return_pptx:
        return prs

    # 출력 PPTX 파일 저장
    prs.save(args.output)
    print(f"PPTX file saved as {args.output}")

if __name__ == "__main__":
    main()
