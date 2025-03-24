import argparse
import json
import os
from copy import deepcopy


def load_json(file_path):
    """JSON 파일을 읽어 딕셔너리로 변환"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def process_json(data):
    NEW_SLIDE = {
        'title': {},
        'layout': 'title_and_content', 
        'placeholders': [[]]
        }

    processed = {}
    processed['frontmatter'] = data['frontmatter']
    processed['slides'] = []
    processed['slides'].append(deepcopy(NEW_SLIDE))
    tokens = data['tokens']
    current_slide = 0
    current_placeholder = 0
    prev_token = {}

    def finalize_slide():
        nonlocal current_slide, current_placeholder # This allows us to modify current_slide
        processed['slides'][current_slide]['layout'] = determine_layout(processed['slides'][current_slide])
        current_slide += 1
        current_placeholder = 0

        processed['slides'].append(deepcopy(NEW_SLIDE))

    def determine_layout(slide):
        print(slide)
        return ''  

    # determine_layout은 빈 슬라이드를 지우는 역할도 하게될 것.

    # def add_token(token, cunsume_type="shared"):
    #     nonlocal current_placeholder, current_slide, prev_token
    #     # is current placeholder empty?
    #     if len(processed['slides'][current_slide]['placeholders'][current_placeholder]) == 0:
    #         processed['slides'][current_slide]['placeholders'][current_placeholder].append(token)
    #     elif (prev_token.get('consume_type') == 'shared' and cunsume_type == 'shared'):
    #         processed['slides'][current_slide]['placeholders'][current_placeholder].append(token)
    #     else:
    #         add_placeholder()
    #         processed["slides"][current_slide]["placeholders"][current_placeholder].append(token)
    #     prev_token = token.extend({'consume_type': cunsume_type})

    def add_token(token, consume_type="shared"):
        nonlocal current_placeholder, current_slide, prev_token

        is_shared = lambda t: t.get("consume_type") == "shared"
        placeholder = processed["slides"][current_slide]["placeholders"][current_placeholder]

        if not placeholder or (is_shared(prev_token) and consume_type == "shared"):
            pass  # 기존 placeholder 그대로 사용
        else:
            add_placeholder()

        # 항상 최신 placeholder로 갱신해서 append
        placeholder = processed["slides"][current_slide]["placeholders"][current_placeholder]
        placeholder.append(token)

        prev_token = {"consume_type": consume_type, **token}

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
                        add_token(
                            {"type": "paragraph", "runs": paragraph(token["children"])}
                        )
                    case 'image':
                        alt = child["children"][0]["raw"]
                        alt_dict = {} if alt == "" else {"alt": alt}
                        add_token(
                            {
                                "type": "image",
                                "url": child["attrs"]["url"],
                                **alt_dict
                            },
                            consume_type="monopoly"
                        )
            case _:
                pass

    return processed  # 중간 처리 로직을 여기에 추가 가능


def save_json(data, export_filename):
    """딕셔너리를 JSON 파일로 저장"""
    with open(export_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON to another JSON format without modification.")
    parser.add_argument("-f", "--file", required=True, help="Input JSON file path")
    parser.add_argument("-e", "--export", nargs="?", const=True, help="Export JSON to file (optional: specify output path)")
    args = parser.parse_args()

    # JSON 파일 로드
    data = load_json(args.file)

    # 중간 처리
    processed_data = process_json(data)

    # 출력 파일명 결정
    if args.export:
        if isinstance(args.export, str):  # -e 옵션에 경로가 주어진 경우
            export_filename = args.export
        else:  # -e 옵션만 사용한 경우, 기본 파일명 사용
            base_name = os.path.splitext(args.file)[0]
            export_filename = f"{base_name}.json"
        
        save_json(processed_data, export_filename)
        print(f"Exported JSON to {export_filename}")
    else:
        print(json.dumps(processed_data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
