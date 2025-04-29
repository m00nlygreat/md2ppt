from pptx import Presentation
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pptx.enum.dml import MSO_THEME_COLOR

color_map = { 
    "Keyword" : MSO_THEME_COLOR.ACCENT_2,
    "Literal" : MSO_THEME_COLOR.ACCENT_1,
    "Name" : MSO_THEME_COLOR.TEXT_1,
    "Operator" : MSO_THEME_COLOR.ACCENT_4,
    "Punctuation" : MSO_THEME_COLOR.ACCENT_5,
    "Comment" : MSO_THEME_COLOR.FOLLOWED_HYPERLINK,
    "Generic" : MSO_THEME_COLOR.ACCENT_6,
    "Text" : MSO_THEME_COLOR.TEXT_1,
    "Background" : MSO_THEME_COLOR.BACKGROUND_1
    }

def highlight_code(code, lang):
    lexer = get_lexer_by_name(lang)
    highlighted = lex(code,lexer)
    return [{'type' : str(ttype).split('.')[1:], 'value': value} for ttype,value in highlighted]

def process_codes(tokens, paragraph):
    for token in tokens:
        r = paragraph.add_run()
        r.text = token.get('value', '')
        type = token.get('type', False)
        if type:
            match(type[0]):
                case 'Literal':
                    r.font.color.theme_color = color_map.get(type[0],MSO_THEME_COLOR.TEXT_1)
                    pass
                case _:
                    r.font.color.theme_color = color_map.get(type[0],MSO_THEME_COLOR.TEXT_1)
                    pass