import argparse
import json
import os
from copy import deepcopy
from urllib import parse


def load_json(file_path):
    """JSON 파일을 읽어 딕셔너리로 변환"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def process_json(data):
    NEW_SLIDE = {
        'title': {},
        'layout': '', 
        'placeholders': [[]],
        'notes': [],
        }

    processed = {}
    processed['frontmatter'] = data['frontmatter']
    processed['slides'] = []
    processed['slides'].append(deepcopy(NEW_SLIDE))
    tokens = data['tokens']
    current_slide = 0
    current_placeholder = 0
    prev_token = {}

    def finalize_slide(finalize_doc=False):
        nonlocal current_slide, current_placeholder # This allows us to modify current_slide
        processed['slides'][current_slide]['layout'] = determine_layout(processed['slides'][current_slide])
        current_slide += 1
        current_placeholder = 0
        if not finalize_doc:
            processed['slides'].append(deepcopy(NEW_SLIDE))

    def determine_layout(slide):
        if slide['layout'] != '':
            return slide['layout']
        
        count_placeholders = 0
        for placeholder in slide['placeholders']:
            if len(placeholder) > 0:
                count_placeholders += 1

        layout = ""

        match(count_placeholders):
            case 0:
                layout = "section_header"                
                pass
            case 1:
                layout = "title_and_content"
                pass
            case 2:
                first = slide['placeholders'][0][0]['consume'] != "monopoly"
                second = slide['placeholders'][1][0]['consume'] != "monopoly"
                if first and second:
                    layout = "two_content"
                else:
                    layout = "content_with_caption"
                pass
            case _:
                layout = ""
        
        return layout

    def add_token(token, consume="shared"):
        nonlocal current_placeholder, current_slide, prev_token

        is_shared = lambda t: t.get("consume") == "shared"
        placeholder = processed["slides"][current_slide]["placeholders"][current_placeholder]

        if not placeholder or (is_shared(prev_token) and consume == "shared"):
            pass  # 기존 placeholder 그대로 사용
        else:
            add_placeholder()

        # 항상 최신 placeholder로 갱신해서 append
        placeholder = processed["slides"][current_slide]["placeholders"][current_placeholder]
        placeholder.append({**token, "consume": consume})

        prev_token = {"consume": consume, **token}

    def add_placeholder():
        nonlocal current_placeholder, current_slide
        processed['slides'][current_slide]['placeholders'].append([])
        current_placeholder += 1

    def paragraph(children):
        def process_token(token, current_style):
            new_style = current_style.copy()
            token_type = token.get('type')
            if token_type == 'strong':
                new_style['bold'] = True
            elif token_type == 'emphasis':
                new_style['italic'] = True
            elif token_type == 'codespan':
                new_style['monospace'] = True
            elif token_type == 'link':
                if 'attrs' in token and 'url' in token['attrs']:
                    new_style['hyperlink'] = token['attrs']['url']
            runs = []
            if 'raw' in token:
                runs.append({**new_style, 'text': token['raw']})
            if 'children' in token:
                for child in token['children']:
                    runs.extend(process_token(child, new_style))
            return runs

        all_runs = []
        for token in children:
            all_runs.extend(process_token(token, {}))
        return all_runs

    def process_list(list_token, ordered=False):
        def iter_token(token, depth=0, ordered=ordered):
            token_type = token.get("type")

            if token_type == "list":
                # 리스트 토큰을 만나면 depth를 1 증가시키고 자식 항목들을 평탄하게 반환합니다.
                new_depth = depth + 1
                items = []
                ordered = token.get("attrs", {}).get("ordered", False)
                for child in token.get("children", []):
                    result = iter_token(child, new_depth, ordered)
                    if result:
                        if isinstance(result, list):
                            items.extend(result)
                        else:
                            items.append(result)
                return items

            elif token_type == "list_item":
                # list_item 내부에서:
                # - 블록 텍스트는 현재 depth의 list_item으로 변환합니다.
                # - 자식 중 리스트가 있다면, 현재 depth를 그대로 넘깁니다.
                runs = None
                extra_items = []
                for child in token.get("children", []):
                    if child.get("type") == "list":
                        # 중첩 리스트: 여기서는 depth를 증가시키지 않고, iter_token의 list 처리에서 증가됩니다.
                        nested = iter_token(child, depth)
                        if nested:
                            if isinstance(nested, list):
                                extra_items.extend(nested)
                            else:
                                extra_items.append(nested)
                    elif child.get("type") == "block_text":
                        runs = paragraph(child.get("children", []))
                    else:
                        processed = iter_token(child, depth)
                        if processed:
                            if isinstance(processed, list):
                                extra_items.extend(processed)
                            else:
                                extra_items.append(processed)
                result = []
                if runs:
                    result.append({"type": "list_item", "depth": depth, "runs": runs, "ordered": ordered})
                result.extend(extra_items)
                return result

            elif token_type == "block_text" or token_type == "paragraph":
                # 단순 block_text는 현재 depth의 list_item으로 변환합니다.
                return {
                    "type": "list_item",
                    "depth": depth,
                    "runs": paragraph(token.get("children", [])),
                    "ordered": ordered
                }

            return None

        result = []

        for child in list_token.get("children", []):
            processed = iter_token(child, 0)
            if processed:
                if isinstance(processed, list):
                    result.extend(processed)
                else:
                    result.append(processed)

        return {"type": "list", "children": result}
    
    def process_table(table):
        def process_cell(cell):
            return {
                'type': 'cell',
                'runs': paragraph(cell.get('children', [])),
                'align': cell.get('attrs', {}).get('align', '')
            }
        head_data = table.get('children',[[]])[0].get('children',False)
        body_data = table.get('children',[[],[]])[1].get('children',False)
        
        result = {
            'type': 'table',
            'head': [],
            'body': [],
        }
        
        if head_data:
            for cell in head_data:
                result['head'].append(process_cell(cell))
        if body_data:
            for row in body_data:
                row_data = []
                for cell in row.get('children', []):
                    row_data.append(process_cell(cell))
                result['body'].append(row_data)
        return result

    for token in tokens:
        type = token['type']

        match(type):
            case "heading":
                level = token["attrs"]["level"]
                match (level):
                    case 1 | 2:
                        finalize_slide()
                        processed["slides"][current_slide]["title"] = {
                            "runs": paragraph(token["children"])
                        }
                    case 3 | 4 | 5 | 6:
                        add_token(
                            {
                                "type": "heading",
                                "level": level,
                                "runs": paragraph(token["children"]),
                            }
                        )
                    case _:
                        pass
            case 'thematic_break':
                finalize_slide()
                processed['slides'][current_slide]['title'] = processed['slides'][current_slide-1]['title']
            case 'wildcard_break':
                add_placeholder()
            case 'block_quote':
                add_token({
                    'type': 'block_quote',
                    'runs': paragraph(token['children'][0]['children'])
                })
            case 'paragraph':
                child = token['children'][0]
                match(child['type']):
                    case "text":
                        # 이 IF문 왜 있는지 나중에 확인
                        if child['raw'] != "":
                            add_token(
                                {"type": "paragraph", "runs": paragraph(token["children"])}
                            )
                    case "link":
                        add_token(
                            {"type": "paragraph", "runs": paragraph(token["children"])}
                        )
                    case 'image':
                        url_o = child["attrs"]["url"]
                        url = url_o if parse.unquote(url_o) == url_o else parse.unquote(url_o)
                        alt = child["children"][0]["raw"]
                        alt_dict = {} if alt == "" else {"alt": alt}
                        add_token(
                            {
                                "type": "image",
                                "url": url,
                                **alt_dict
                            },
                            consume="monopoly"
                        )
            case 'list':
                add_token(process_list(token,token.get("attrs", {}).get("ordered", False)))
            case 'block_code':
                add_token(
                    {
                        "type": "code",
                        "lang": token.get("attrs", {}).get("info", ""),
                        "raw": token["raw"],
                    }
                )
            case 'comment_block':
                match(token['key']):
                    case 'layout':
                        processed['slides'][current_slide]['layout'] = token['value']
                    case 'note':
                        processed['slides'][current_slide]['notes'].append(token['value'])
            case 'blank_line':
                pass
            case 'table':
                add_token(
                    process_table(token),
                    consume="monopoly"
                )
            case _:
                print(token)
                pass

    finalize_slide(True)
    
    for slide in processed['slides']:
        title_empty = not slide['title']
        placeholder_empty = not slide['placeholders'][0]
        if title_empty and placeholder_empty:
            processed['slides'].remove(slide)            

    return processed 

def save_json(data, export_filename):
    """딕셔너리를 JSON 파일로 저장"""
    with open(export_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to another JSON format without modification.")
    parser.add_argument("-i", "--input", help="Input JSON file path or JSON string")
    parser.add_argument("-o", "--output", help="Output JSON file path (default: {input_filename}.slides.json)")
    parser.add_argument("--return-dict", action="store_true", help="Return dictionary instead of saving to file")
    args = parser.parse_args()

    # 입력 데이터 처리
    if args.input:
        if os.path.exists(args.input):
            # 파일에서 JSON 로드
            data = load_json(args.input)
        else:
            # JSON 문자열로 처리
            try:
                data = json.loads(args.input)
            except json.JSONDecodeError:
                print("Error: Invalid JSON string provided")
                return
    else:
        print("Error: input is required. Use -i or --input to specify input.")
        return

    # 중간 처리
    processed_data = process_json(data)

    # 딕셔너리 반환 모드
    if args.return_dict:
        return processed_data

    # 출력 파일명 결정
    if args.output:
        export_filename = args.output
    else:
        if os.path.exists(args.input):
            base_name = os.path.splitext(args.input)[0]
            export_filename = f"{base_name}.slides.json"
        else:
            export_filename = "output.slides.json"
    
    # JSON 파일로 저장
    save_json(processed_data, export_filename)
    print(f"Exported JSON to {export_filename}")

if __name__ == "__main__":
    main()
