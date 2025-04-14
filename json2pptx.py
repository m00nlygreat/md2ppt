import argparse
from enum import Enum
import json
import os
import re
import tempfile
import warnings
from pptx import Presentation
from pptx.util import Inches

# 중복 경고는 무시 (선택 사항)
warnings.filterwarnings("ignore", message="Duplicate name:")

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

        # placeholder idx와
        p_map = {}
        for i, pl in enumerate(current_slide.placeholders):
            p_map.update({i: pl.placeholder_format.idx})            

        # 제목을 설정합니다.
        title = slide.get("title", {"title": { "runs": [{"text": "제목없음."}]}})
        runs = title.get("runs", [])
        if title:
            title_shape = current_slide.shapes.title
            p = title_shape.text_frame.paragraphs[0]
            process_runs(runs, p)

        pholder_no = 0
        for pholder_data in slide.get("placeholders", []):
            pholder_no += 1
            if len(current_slide.placeholders) > pholder_no:
                # print(current_slide.slide_layout.name)
                # print(token)
                try:
                    current_placeholder = current_slide.placeholders[p_map[pholder_no]]
                except Exception as e:
                    print(e)

                for token in pholder_data:
                    process_token(current_placeholder, token, current_slide)

def process_token(current_placeholder, token, current_slide):
    match(token.get("type", "")):
        case "paragraph":
            p = define_paragraph(current_placeholder)
            process_runs(token.get("runs", []), p)
        case "image":
            url = token.get("url", "")
            try:
                current_placeholder.insert_picture(url)
            except Exception as e:
                left = current_placeholder.left
                top = current_placeholder.top
                width = current_placeholder.width
                height = current_placeholder.height

                sp = current_placeholder._element
                sp.getparent().remove(sp)

                current_slide.shapes.add_picture(url, left, top, width=width, height=height)

        case _ :
            # print(token.get("type", ""))
            pass

def define_paragraph(placeholder):
    """
    Placeholder에서 첫 번째 단락을 가져오고, 텍스트가 비어있으면 새 단락을 추가합니다.
    """
    if placeholder.text_frame.paragraphs[0].text != "":
        paragraph = placeholder.text_frame.add_paragraph()
    else:
        paragraph = placeholder.text_frame.paragraphs[0]
    return paragraph

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
        if 'italic' in run:
            font.italic = True
        if 'monospace' in run:
            font.name = 'Consolas'
            # print(font.size)
            # 현재 폰트 사이즈를 알아내는 게 쉽지 않다.
        if 'hyperlink' in run:
            r.hyperlink.address = run.get("hyperlink", "https://google.com")

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
    args = parser.parse_args()

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

    layouts = get_slide_layout_enum(prs)
    # for layout in layouts:
    #     print(f"{layout.name} = {layout.value}")

    # JSON 데이터를 기반으로 PPTX 변환 로직 실행 (개발자가 직접 구현)
    convert_json_to_pptx(prs, data, layouts=layouts)

    # 출력 PPTX 파일 저장
    prs.save(args.output)
    print(f"PPTX file saved as {args.output}")


if __name__ == "__main__":
    main()
