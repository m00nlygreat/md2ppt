import argparse
import json
import os
import re
import yaml
import mistune
from comment import plugin_comment_block
from wildcard_break import wildcard_break_plugin

def extract_frontmatter(markdown_text: str):
    """
    마크다운 텍스트의 시작 부분에 있는 YAML frontmatter를 추출하여 파싱합니다.
    frontmatter가 있으면 파싱된 딕셔너리와 frontmatter를 제거한 마크다운 텍스트를 반환합니다.
    """
    fm_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    m = re.match(fm_pattern, markdown_text, re.DOTALL)
    frontmatter = {}
    if m:
        fm_text = m.group(1)
        try:
            frontmatter = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print("YAML frontmatter 파싱 오류:", e)
        # frontmatter 블록 제거
        markdown_text = markdown_text[m.end():]
    return frontmatter, markdown_text

def analyze_markdown(markdown_text: str):
    """
    mistune을 사용해 renderer 없이 마크다운 텍스트를 토큰화합니다.
    이 함수는 마크다운 구조를 반영하는 딕셔너리 형태의 토큰들을 반환합니다.
    """
    md = mistune.create_markdown(renderer=None, plugins=[plugin_comment_block, wildcard_break_plugin])
    tokens = md(markdown_text)
    print("✅ Registered Plugins:", md.block.rules)
    return tokens

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to JSON dictionary using mistune.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to the Markdown file")
    group.add_argument("markdown", nargs="?", help="Markdown string input")
    parser.add_argument("-e", "--export", action="store_true", help="Export output to a JSON file")
    args = parser.parse_args()

    # 파일 또는 인자로부터 마크다운 내용 읽기
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: file '{args.file}' does not exist.")
            return
        with open(args.file, "r", encoding="utf-8") as md_file:
            md_content = md_file.read()
    else:
        md_content = args.markdown

    # YAML frontmatter 추출 및 제거
    frontmatter, remaining_text = extract_frontmatter(md_content)
    
    # 나머지 마크다운 내용 토큰화
    tokens = analyze_markdown(remaining_text)

    # 최종 출력 딕셔너리에 frontmatter와 토큰들을 추가
    output = {
        "frontmatter": frontmatter,
        "tokens": tokens
    }

    if args.export:
        if args.file:
            base_name = os.path.splitext(args.file)[0]
            out_filename = base_name + ".json"
        else:
            out_filename = "output.json"
        with open(out_filename, "w", encoding="utf-8") as json_file:
            json.dump(output, json_file, indent=4, ensure_ascii=False)
        print(f"Exported JSON to {out_filename}")
    else:
        print(json.dumps(output, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
