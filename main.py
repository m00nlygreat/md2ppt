#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from md2json import process_markdown
from json2slide import process_json
from json2pptx import main as json2pptx_main
from flatten import flatten_markdown

def save_debug_data(data, filename):
    """디버그 데이터를 JSON 파일로 저장합니다."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Debug data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to PPTX using a pipeline of processors.")
    parser.add_argument("-i", "--input", required=True, help="Input Markdown file path")
    parser.add_argument("-o", "--output", help="Output PPTX file path (default: {input_filename}.pptx)")
    parser.add_argument("-d", "--debug", action="store_true", help="Save intermediate processing results to files")
    parser.add_argument("--debug-dir", default="debug", help="Directory to save debug files (default: 'debug')")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_ref = os.path.join(script_dir, "refs", "default.pptx")
    parser.add_argument("-r","--ref", help="Reference PPTX file path for styling", default=default_ref)
    args = parser.parse_args()

    # 입력 파일 확인
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return 1

    # 디버그 디렉토리 생성
    if args.debug and not os.path.exists(args.debug_dir):
        os.makedirs(args.debug_dir)

    # 출력 파일 경로 결정
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(args.input)[0]
        output_file = f"{base_name}.pptx"

    try:
        # 1. flatten 파이프라인 적용
        print(f"Flattening Markdown file: {args.input}")
        flattened_md = flatten_markdown(args.input, is_root=True)
        if args.debug:
            debug_flatten_file = os.path.join(args.debug_dir, "0_flattened.md")
            with open(debug_flatten_file, "w", encoding="utf-8") as f:
                f.write(flattened_md)

        # 2. 마크다운을 JSON 딕셔너리로 변환
        print("Converting Markdown to JSON...")
        json_data = process_markdown(flattened_md)
        
        # 디버그 모드에서 중간 결과 저장
        if args.debug:
            debug_json_file = os.path.join(args.debug_dir, "1_markdown_to_json.json")
            save_debug_data(json_data, debug_json_file)

        # 3. JSON 딕셔너리를 슬라이드 딕셔너리로 변환
        print("Converting JSON to slide format...")
        slide_data = process_json(json_data)
        
        # 디버그 모드에서 중간 결과 저장
        if args.debug:
            debug_slide_file = os.path.join(args.debug_dir, "2_json_to_slide.json")
            save_debug_data(slide_data, debug_slide_file)

        # 4. 슬라이드 딕셔너리를 PPTX로 변환
        print("Converting slide format to PPTX...")
        # json2pptx_main 함수에 필요한 매개변수를 직접 전달
        # 참조 PPTX 파일 경로와 출력 파일 경로는 환경 변수로 설정
        os.environ["JSON2PPTX_REF"] = args.ref if args.ref else ""
        os.environ["JSON2PPTX_OUTPUT"] = output_file
        os.environ["JSON2PPTX_RETURN_PPTX"] = "1"
        
        # json2pptx_main 함수 호출
        pptx_obj = json2pptx_main(data=slide_data)

        # 5. PPTX 파일 저장
        print(f"Saving PPTX file: {output_file}")
        pptx_obj.save(output_file)
        print(f"Successfully converted {args.input} to {output_file}")

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 