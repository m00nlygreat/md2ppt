---
role: "현재 요구사항 요약의 유지본"
usage: "요구사항을 정리하거나 갱신할 때 함께 관리한다. 원본 자료를 그대로 복사하지 말고 현재 합의된 요구사항을 짧게 요약한다."
---

# 요구사항 요약

## 1. 입력 처리

- Markdown 파일을 입력받아 PowerPoint 프레젠테이션으로 변환한다.
- YAML frontmatter를 읽어 제목 슬라이드와 메타데이터 처리에 사용한다.
- Obsidian 스타일의 첨부 이미지 경로와 Markdown 이미지 참조를 처리한다.
- Markdown 본문을 토큰 JSON으로 변환한다.

## 2. 슬라이드 구조화

- H1/H2 heading은 새 슬라이드와 TOC 항목 생성에 사용한다.
- H3 이하 heading은 현재 슬라이드의 콘텐츠로 처리한다.
- thematic break는 새 슬라이드 구분자로 처리한다.
- wildcard break는 현재 슬라이드 안의 새 placeholder 구분자로 처리한다.
- paragraph, list, table, image, block quote, code block을 placeholder 콘텐츠로 구조화한다.
- note comment block은 슬라이드 노트로 구조화한다.

## 3. Layout 처리

- `[layout]: # (layout_name)` comment block으로 슬라이드 layout을 명시할 수 있다.
- 명시된 layout은 자동 layout 판정보다 우선한다.
- layout이 명시된 빈 슬라이드는 삭제하지 않고 해당 layout을 적용한다.
- layout이 없는 슬라이드는 placeholder 구성에 따라 자동 layout을 판정한다.
- layout 자동 판정은 빈 슬라이드 제거 이후 남은 슬라이드에만 적용한다.

## 4. 빈 슬라이드와 TOC

- 제목, placeholder 콘텐츠, layout이 모두 없는 슬라이드는 제거한다.
- 빈 슬라이드 제거 후 TOC의 chapter/module slide index를 남은 슬라이드 기준으로 보정한다.
- TOC 슬라이드는 사용 가능한 TOC layout이 있으면 사용하고, 없으면 기본 대체 layout을 사용한다.
- TOC 항목에는 대상 슬라이드 링크를 설정한다.

## 5. PPTX 생성과 템플릿

- slide JSON을 python-pptx로 변환해 PPTX 파일을 생성한다.
- 제목 슬라이드는 frontmatter 기반으로 생성한다.
- 내장 PowerPoint 템플릿은 패키지 데이터로 제공한다.
- `--template`은 내장 템플릿 이름을 선택한다.
- `--list-templates`는 사용 가능한 내장 템플릿 이름을 출력한다.
- `--ref`는 사용자가 직접 제공하는 PPTX 템플릿 경로를 사용한다.
- `--ref`가 지정되면 `--template`보다 우선한다.

## 6. Template/Ref PPT 메타정보

- PPTX 템플릿의 slide layout 이름은 Markdown의 layout 이름과 매칭 가능한 기준으로 관리한다.
- 내장 템플릿과 사용자가 제공한 `--ref` PPTX 모두 동일한 메타정보 규칙을 따른다.

## 7. Placeholder 이름 JSON 메타정보

- layout placeholder 도형 이름에는 JSON 문자열로 메타정보를 넣을 수 있다.
- PPT 생성 시 placeholder 이름을 JSON으로 파싱하고, 파싱된 값을 해당 placeholder의 배치 보조 정보로 사용한다.
- JSON 메타정보가 없거나 파싱할 수 없으면 해당 placeholder는 기본 위치와 크기 규칙을 사용한다.
- JSON 메타정보는 객체 형식이어야 한다. 예: `{"align": 5, "grow": true}`.
- `align`은 이미지가 placeholder 영역 안에 배치되는 기준점으로 사용한다.
- `grow`는 콘텐츠 placeholder가 남은 공간을 채우도록 크기를 조정할지 판단하는 값으로 사용한다.
- JSON 메타정보는 placeholder의 실제 위치, 크기, 이름 정보와 병합되어 후속 배치 계산에 사용한다.
- JSON 메타정보는 템플릿 제작자가 PPT 편집 화면에서 placeholder 도형 이름에 직접 기록한다.

## 8. 디버그와 출력

- 기본 출력 파일명은 입력 Markdown 파일명을 기준으로 생성한다.
- 디버그 모드에서는 Markdown 파싱 결과와 slide JSON 중간 산출물을 저장한다.
- CLI 실행 결과로 최종 PPTX 파일을 저장한다.
