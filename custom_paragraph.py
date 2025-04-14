from pptx.text.text import _Paragraph
from lxml import etree

class CustomParagraph(_Paragraph):
    @property
    def bullet(self):
        # bullet 속성의 getter가 필요하다면 구현 (여기서는 생략)
        pass

    @bullet.setter
    def bullet(self, value):
        # self._p는 paragraph의 내부 XML 요소
        pPr = self._p.get_or_add_pPr()
        # bullet 폰트 요소가 있는지 확인
        if pPr.find(
            "a:buFont", 
            namespaces={"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        ) is None:
            # 없으면 Wingdings 폰트를 기본 bullet 폰트로 생성
            buFont = etree.Element(
                "{http://schemas.openxmlformats.org/drawingml/2006/main}buFont",
                typeface="Wingdings",
                pitchFamily="2",
                charset="2",
                panose="05000000000000000000",
            )
            pPr.insert(0, buFont)
        # bullet 속성에 전달받은 값 할당 (예를 들어, True 또는 특정 값)
        pPr.bullet = value