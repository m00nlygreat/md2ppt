from pptx import Presentation
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Inches

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
    if lang:
        lexer = get_lexer_by_name(lang)
    else:
        lexer = guess_lexer(code)
    highlighted = lex(code,lexer)
    return [{'type' : str(ttype).split('.')[1:], 'value': value} for ttype,value in highlighted]

def process_codes(tokens, paragraph):
    def needs_rstrip(text):
        return text != text.rstrip(" \n")
    def normalize_blank_line(text):
        if text == "\n" or text == "\r\n":
            return " \n"
        return text
    while tokens[-1].get('value', '') == '\n':
        tokens.pop(-1)
    while tokens[0].get('value', '') == '\n':
        tokens.pop(0)
    while needs_rstrip(tokens[-1].get('value', '')):
        tokens[-1]['value'] = tokens[-1]['value'].rstrip(" \n")

    paragraph.space_before = Inches(0.1)
    for token in tokens:
        r = paragraph.add_run()
        r.text = normalize_blank_line(token.get('value', ''))
        type = token.get('type', False)
        if type:
            match(type[0]):
                case 'Literal':
                    r.font.color.theme_color = color_map.get(type[0],MSO_THEME_COLOR.TEXT_1)
                    pass
                case _:
                    r.font.color.theme_color = color_map.get(type[0],MSO_THEME_COLOR.TEXT_1)
                    pass
            paragraph.space_before = Inches(0)
