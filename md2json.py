import argparse
import json
import os
import re
import yaml
import mistune
from utils.comment import plugin_comment_block
from utils.wildcard_break import wildcard_break_plugin

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
    # print("✅ Registered Plugins:", md.block.rules)
    return tokens

def process_markdown(markdown_text: str):
    """
    마크다운 텍스트를 처리하여 딕셔너리 형태로 반환합니다.
    파일 입출력 없이 직접 딕셔너리를 반환합니다.
    """
    # YAML frontmatter 추출 및 제거
    frontmatter, remaining_text = extract_frontmatter(markdown_text)
    
    # 나머지 마크다운 내용 토큰화
    tokens = analyze_markdown(remaining_text)

    # 최종 출력 딕셔너리에 frontmatter와 토큰들을 추가
    return {
        "frontmatter": frontmatter,
        "tokens": tokens
    }

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to JSON dictionary using mistune.")
    parser.add_argument("-i", "--input", help="Path to the Markdown file or Markdown string input")
    parser.add_argument("-o", "--output", help="Output JSON file path (default: {input_filename}.json)")
    parser.add_argument("--return-dict", action="store_true", help="Return dictionary instead of saving to file")
    args = parser.parse_args()

    if not args.input:
        print("Error: input is required. Use -i or --input to specify input.")
        return

    # 파일 경로인지 마크다운 문자열인지 확인
    if os.path.exists(args.input):
        # 파일로부터 마크다운 내용 읽기
        with open(args.input, "r", encoding="utf-8") as md_file:
            md_content = md_file.read()
    else:
        # 마크다운 문자열로 처리
        md_content = args.input

    # 마크다운 처리
    output = process_markdown(md_content)

    # 딕셔너리 반환 모드
    if args.return_dict:
        return output

    # 출력 파일 경로 결정
    if args.output:
        out_filename = args.output
    else:
        if os.path.exists(args.input):
            base_name = os.path.splitext(args.input)[0]
            out_filename = base_name + ".json"
        else:
            out_filename = "output.json"
    
    # JSON 파일로 저장
    with open(out_filename, "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)
    print(f"Exported JSON to {out_filename}")

if __name__ == "__main__":
    main()
