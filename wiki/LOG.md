---
role: "프로젝트 관련 중대 결정사항, 새로 알아낸 사실, 방향 변경의 시간순 기록"
usage: "중요한 결정, 새 사실, 범위 변경, 설계 방향 변경이 생기면 날짜별 항목으로 짧게 추가한다. 사소한 작업 로그나 명령 실행 기록은 남기지 않는다."
---

# LOG

프로젝트 관련 중대 결정사항, 새로 알아낸 사실, 방향 변경을 시간순으로 기록한다.

## 2026-06-03

- 내장 PowerPoint 템플릿은 루트 파일이 아니라 Python 패키지 데이터로 관리한다.
- 내장 템플릿은 `--template`과 `--list-templates`로 이름 기반 접근을 제공하고, `--ref`는 사용자 제공 PPTX 경로에만 사용한다.
- layout이 명시된 빈 슬라이드는 삭제하지 않고 해당 layout을 적용하기로 했다.
- layout 자동 판정은 빈 슬라이드 제거 이후 남은 슬라이드에만 적용한다.
- 프로젝트 위키 문서로 [요구사항](wiki/REQUIREMENT.md)과 [변경 로그](wiki/LOG.md)를 유지한다.
- [요구사항](wiki/REQUIREMENT.md)은 제품 설명보다 기능 요구사항에 한정해 유지한다.
- [요구사항](wiki/REQUIREMENT.md)에 Template/Ref PPT 메타정보 요구사항을 추가했다.
- 도형 이름 JSON 메타정보의 `id`, `show_anyway`로 named shape 텍스트 입력과 조건부 제거를 지원한다.
- 제목 슬라이드 named shape는 YAML frontmatter 값을 사용하고, 같은 `id` 도형 여러 개에 동일 입력을 적용한다.
- `--no-toc` 옵션으로 TOC 슬라이드 생성을 건너뛸 수 있게 한다.
