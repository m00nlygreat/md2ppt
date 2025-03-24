import sys
from pptx import Presentation

def print_master_slide_layouts(pptx_path):
    """PPTX 파일을 열고 모든 마스터 슬라이드의 레이아웃 이름을 출력"""
    try:
        presentation = Presentation(pptx_path)  # PPTX 파일 열기
        for master in presentation.slide_masters:
            print(f"마스터 슬라이드: {master.name}")
            for layout in master.slide_layouts:
                print(f"  - 레이아웃 이름: {layout.name}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python script.py <PPTX 파일 경로>")
        sys.exit(1)

    pptx_file_path = sys.argv[1]  # 첫 번째 명령줄 인수로 파일 경로 받기
    print_master_slide_layouts(pptx_file_path)
