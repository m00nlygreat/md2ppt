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
- `--no-toc` 옵션을 지정하면 TOC 슬라이드를 생성하지 않는다.

## 5. PPTX 생성과 템플릿

- slide JSON을 python-pptx로 변환해 PPTX 파일을 생성한다.
- 제목 슬라이드는 frontmatter 기반으로 생성한다.
- 내장 PowerPoint 템플릿은 패키지 데이터로 제공한다.
- `--template`은 내장 템플릿 이름을 선택한다.
- `--list-templates`는 사용 가능한 내장 템플릿 이름을 출력한다.
- `--ref`는 사용자가 직접 제공하는 PPTX 템플릿 경로를 사용한다.
- `--ref`가 지정되면 `--template`보다 우선한다.
- `--no-toc`은 Markdown to PPTX CLI와 JSON to PPTX CLI에서 모두 사용할 수 있다.

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

## 8. Named Shape JSON 메타정보

- 도형 이름 JSON 메타정보에는 named shape 식별자 `id`를 넣을 수 있다.
- Markdown comment block `[id]: # (텍스트)`는 같은 `id`를 가진 도형의 text frame에 입력된다.
- 제목 슬라이드의 named shape 입력은 YAML frontmatter의 같은 key 값을 사용한다.
- named shape 입력 값은 inline Markdown으로 처리해 bold, italic, link, codespan runs를 반영한다.
- `show_anyway: false`인 도형은 같은 `id` 입력이 없으면 PPT 결과에서 제거한다.
- `show_anyway: true`이거나 `show_anyway`가 생략된 도형은 같은 `id` 입력이 없어도 유지한다.
- 같은 `id` 입력이 있으면 `show_anyway` 값과 무관하게 도형을 유지하고 텍스트를 입력한다.
- 한 슬라이드에 같은 `id`를 가진 도형이 여러 개 있으면 같은 입력 값을 모두 적용한다.
- 표시하지 않는 도형은 hidden 처리하지 않고 XML에서 제거한다.

## 9. 디버그와 출력

- 기본 출력 파일명은 입력 Markdown 파일명을 기준으로 생성한다.
- 디버그 모드에서는 Markdown 파싱 결과와 slide JSON 중간 산출물을 저장한다.
- CLI 실행 결과로 최종 PPTX 파일을 저장한다.

## 10. 웹 발표 모드

- 기존 PPTX 변환을 유지하며 `md2ppt serve -i deck.md`로 로컬 웹서버를 실행해 발표한다.
- 같은 Markdown의 embed flatten, 슬라이드 구분, placeholder와 layout 해석을 재사용한다.
- PPTX와 웹 출력은 공통 slide JSON을 사용한다.
- 화면은 16:9 슬라이드를 기준으로 확대·축소하고, 디자인은 별도 HTML/CSS 웹 테마로 제공한다.
- PPTX 템플릿의 글꼴·좌표·도형을 그대로 복제하지 않는다.
- 표지·목차·본문, 제목·목록·표·인용문·코드·이미지와 기본 레이아웃을 표시한다.
- 이전·다음 버튼, 방향키, PageUp/PageDown, Home/End, 전체화면, 슬라이드 번호, URL 위치 복원을 제공한다.
- `--no-toc`은 웹에서도 목차 슬라이드 생성을 생략한다.
- 원본 변경은 브라우저 새로고침으로 반영한다. 자동 감지는 후속 범위로 두고, 발표자 화면은 Reveal.js 전환 계획에 포함한다.
- PPTX named shape 입력은 웹에서 지원하지 않고 경고한다. raw HTML은 실행하지 않으며 위험한 링크 scheme을 차단한다.
- 웹 정적 파일은 Python 패키지 데이터로 제공하고, 기존 CLI·내장 템플릿·`--ref` 기능을 유지한다.

## 11. 웹 CSS 테마

- 슬라이드 레이아웃과 표지·목차·본문·콘텐츠·발표 UI의 스타일을 외부 CSS로 정의한다.
- 기본 테마는 프로젝트 루트의 [styles/default.css](../styles/default.css)에 저장한다.
- `md2ppt serve -i deck.md --theme <CSS 경로>`로 기본 테마를 교체할 수 있다.
- 옵션을 생략하면 실행 위치와 관계없이 기본 테마를 제공한다. 배포본에도 같은 기본 CSS를 포함한다.
- 사용자 CSS의 상대 경로는 현재 작업 디렉터리를 기준으로 해석하고, 잘못된 경로는 서버 시작 전에 오류로 알린다.
- 선택한 CSS는 HTTP로 제공하며, 수정 후 브라우저 새로고침으로 변경을 반영한다.
- CSS는 매 요청 UTF-8로 다시 읽고, 파일을 읽지 못하면 경로와 원인을 로그에 남긴다.
- 렌더러는 레이아웃·placeholder 수·표 정렬을 클래스와 `data-*` 메타정보로 제공한다. 배치는 테마 CSS에서 정한다.
- 기본 테마의 기준 크기는 `--stage-width`, `--stage-height`로 정의한다. Reveal.js 전환 후에는 이 값을 Reveal 설정에 전달해 화면 배율을 관리한다.
- 기본 CSS 한 파일을 소스 실행과 패키지 설치 환경에서 함께 사용한다.
- Reveal.js 전환 시 핵심 CSS는 항상 로드하고, `--theme`은 그 위의 md2ppt 테마 CSS를 교체한다.
- 기존 사용자 CSS의 자체 stage·active 상태·배율 규칙을 새 구조로 옮기는 방법을 안내한다.

## 12. Reveal.js 전환 (구현 완료)

- 웹 발표 엔진을 Reveal.js 6.0.2로 교체하고, Markdown 해석·slide JSON·콘텐츠 HTML 생성은 md2ppt가 담당한다.
- 슬라이드 이동·표시 상태·화면 배율·진행 표시·전체 슬라이드 보기는 Reveal.js에 맡긴다.
- 기존 노트를 안전한 HTML로 렌더링해 공식 Notes 플러그인의 노트·현재/다음 슬라이드·타이머에 연결한다.
- 새 슬라이드 주소는 `#/slide-N`으로 정하고, 기존 `#slide=N` 주소도 초기 변환으로 지원한다.
- 기존 입력 문법, CLI 옵션, 기본 레이아웃과 PPTX 변환 기능을 유지한다.
- 콘텐츠 맞춤과 넘침 안내는 Reveal 이벤트에 연결하며 자체 stage 배율과 발표 상태 관리를 제거한다.
- 고정 버전의 JS·CSS·LICENSE·출처와 해시를 Python 패키지에 포함한다. 사용자는 Node.js나 CDN 없이 실행한다.
- 발표자 미리보기는 같은 origin만 허용하고, Notes의 고정 인라인 스크립트만 CSP hash로 허용한다.
- 고정 버전 리소스와 기본 발표자 화면은 Node.js·CDN 없이 로컬에서 실행하고, 패키지 wheel·sdist에 포함한다.
- 상세 구현 순서와 검증·완료 기준은 [Reveal.js 전환 계획](../PLAN.md)에 둔다.
