import json
from lxml import etree
from pptx.enum.lang import MSO_LANGUAGE_ID
from pptx.oxml.xmlchemy import OxmlElement

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
        "right": shape.left + shape.width,
        "bottom": shape.top + shape.height,
        **from_pl,
    }