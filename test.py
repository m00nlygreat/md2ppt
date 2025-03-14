import mistune
import sys
import json

# 커맨드 라인 인자 확인
if len(sys.argv) < 2:
    print("사용법: python test.py <markdown_file_path> [--export]")
    sys.exit(1)

# 파일 경로
file_path = sys.argv[1]
export_mode = "--export" in sys.argv

try:
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 마크다운을 파싱
    md = mistune.create_markdown(renderer=None)
    result = md(content)
    
    # 결과 출력 또는 파일로 저장
    if export_mode:
        output_file = file_path.rsplit('.', 1)[0] + '.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"파싱 결과가 '{output_file}'로 저장되었습니다.")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

except FileNotFoundError:
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {str(e)}")
