import argparse
import os
import json
import yaml


def convert_json_to_yaml(json_path, export_path=None):
    # JSON 파일 읽기
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 출력 파일 경로 결정
    if export_path is None:
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        export_path = base_name + ".yaml"

    # YAML 파일로 저장
    with open(export_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"✅ YAML exported to: {export_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert a JSON file to YAML format.")
    parser.add_argument(
        "-f", "--file", required=True, help="Path to the input JSON file"
    )
    parser.add_argument(
        "-e",
        "--export",
        nargs="?",
        const=True,
        help="Export to YAML (optionally provide output path)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ Error: file '{args.file}' not found.")
        return

    # 처리 분기
    if args.export:
        export_path = args.export if isinstance(args.export, str) else None
        convert_json_to_yaml(args.file, export_path)
    else:
        print("ℹ️ No export requested. Use -e to export to YAML.")


if __name__ == "__main__":
    main()
