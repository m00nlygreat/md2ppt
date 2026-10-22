# Reveal.js 웹 프레젠터 전환 계획

- 작성일: 2026-10-22
- 상태: 구현 완료
- 목적: Markdown 해석과 콘텐츠 HTML 생성은 md2ppt가 담당하고, 브라우저 발표 기능은 Reveal.js로 제공한다.
- 기준 버전: [Reveal.js 6.0.2](https://github.com/hakimel/reveal.js/releases/tag/6.0.2). 이번 전환에서는 버전을 고정한다.

## 1. 전환 목표와 역할

기존 자체 플레이어를 Reveal.js로 교체한다. 기존 Markdown 문법과 PPTX·웹 공통 slide JSON을 재사용하며, Reveal.js에는 완성된 슬라이드 HTML을 전달한다.

| 담당 | 범위 |
| --- | --- |
| md2ppt 파이프라인 | Obsidian embed flatten, frontmatter, 슬라이드 구분, layout·placeholder·목차·노트 해석 |
| md2ppt 렌더러 | 표지·목차·본문·노트 HTML, 안전한 링크·텍스트 처리, 로컬 이미지 등록, Pygments 코드 강조 |
| md2ppt CSS | 본문 레이아웃, 글꼴·색상·표·코드·이미지, 문서 진단과 콘텐츠 넘침 안내 |
| Reveal.js | 슬라이드 표시 상태, 이동·단축키·터치, URL 위치, 화면 확대·축소, 전체 슬라이드 보기, 진행 표시, 발표자 화면 |
| 연결 스크립트 | Reveal 초기화, 기존 링크 변환, 버튼 연결, 콘텐츠 맞춤과 진단 연동 |

Reveal의 Markdown·구문 강조 플러그인은 로드하지 않는다. 콘텐츠를 브라우저에서 다시 파싱하지 않고, 기존 서버 렌더링 결과를 사용한다.

## 2. 사용자 동작과 CLI

기존 명령과 옵션을 그대로 사용한다.

```sh
md2ppt serve -i deck.md
md2ppt serve -i deck.md --theme "./styles/company.css"
md2ppt serve -i deck.md --host 127.0.0.1 --port 3000 --no-toc
md2ppt serve -i "D:/vault/강의/아는 만큼 쓰는 ChatGPT.md"
```

- `-i`, `--host`, `--port`, `--no-toc`, `--theme`의 의미와 경로 검증을 유지한다.
- 이전·다음은 Reveal 기본 controls를 사용하고, 슬라이드 번호와 진행 막대를 표시한다.
- 방향키, PageUp/PageDown, Home/End, 터치 이동과 전체 화면을 지원한다.
- 전체 화면은 `F`와 화면 버튼으로, 발표자 보기는 `S`와 화면 버튼으로 연다.
- `Esc`로 전체 슬라이드를 보고 선택한 슬라이드로 이동할 수 있게 한다.
- 입력창·링크·버튼을 조작하는 동안에는 발표 단축키가 해당 조작을 가로채지 않게 한다.
- 기본 화면은 1280×720의 16:9이며, 좁은 화면에서도 자동 scroll view로 바뀌지 않게 한다.
- 초기 전환 효과는 `none`으로 정하고 Reveal 기본 발표 모드에서 동작시킨다.
- Markdown·이미지·CSS 수정은 새로고침으로 반영한다. 새로고침 시 현재 위치를 복원한다.
- 사용자는 Node.js 설치나 별도의 프런트엔드 빌드 없이 Python 패키지만 설치해 실행한다.

## 3. Reveal.js 리소스와 배포

[Reveal.js 리소스 폴더](md2ppt/web/assets/vendor/reveal/)를 만들고 공식 6.0.2 배포본의 필요한 파일을 포함한다.

- 핵심 리소스는 `dist/reveal.js`, `dist/reveal.css`, `dist/plugin/notes.js`다. 파일 경로는 6.0.2 배포 구조를 따른다.
- 공식 빌드 결과물을 사용하고 라이브러리 코드를 직접 수정하지 않는다.
- 버전, 배포 출처, 포함 파일 목록과 SHA-256, 발표자 화면에 필요한 CSP hash를 배포 메타정보로 기록한다.
- 원본 MIT LICENSE와 저작권 고지를 포함하고 리소스 갱신 절차를 README에 적는다.
- CDN이나 실행 시 다운로드에 의존하지 않는다. 로컬 문서·이미지로 구성된 발표는 인터넷 없이 실행할 수 있어야 한다.
- 서버는 패키지 리소스를 명시적인 URL 목록에 연결한다. vendor 폴더 전체를 임의 파일 탐색 경로로 노출하지 않는다.
- 필요한 리소스가 없으면 서버 시작 전에 파일과 원인을 알리고 실패한다.
- [패키지 설정](pyproject.toml)과 [소스 배포 설정](MANIFEST.in)에 중첩된 JS·CSS·라이선스·배포 메타정보를 포함한다.
- [기본 테마 빌드 훅](md2ppt_build.py)의 단일 CSS 원본 방식을 유지하며 wheel·sdist에도 동일한 리소스를 넣는다.

## 4. HTML 렌더러 전환

[웹 렌더러](md2ppt/web/render.py)의 바깥 구조를 Reveal 규칙에 맞춘다.

```html
<div class="reveal">
  <div class="slides">
    <section id="slide-1" class="slide cover-slide">...</section>
    <section id="slide-2" class="slide toc-slide">...</section>
    <section id="slide-3" class="slide body-slide layout-two_content">
      <div class="slide-inner">...</div>
      <aside class="notes">...</aside>
    </section>
  </div>
</div>
```

- 슬라이드마다 하나의 최상위 `section`을 만들고, 중첩 section으로 수직 슬라이드가 생기지 않게 한다.
- 표지·목차·본문의 순서와 `--no-toc` 처리, 빈 슬라이드 제거 후 보정된 목차 index를 유지한다.
- 각 슬라이드에 1부터 시작하는 `slide-N` ID를 부여한다. 번호에는 표지와 선택적으로 생성되는 목차도 포함한다.
- 기존 `slide-inner`, `slide-heading`, `slide-content`, `placeholder`, layout 클래스와 `data-layout`, `data-slot-count`, `data-slot-columns`, `data-align`을 유지한다.
- 문서 진단과 보조 버튼은 슬라이드 목록 밖에 두어 별도 슬라이드로 계산되지 않게 한다.
- 제목·강조·링크·중첩 목록·표·인용문·코드·이미지·누락 자산 안내를 기존 렌더링 규칙으로 생성한다.
- 본문과 노트 모두 raw HTML 실행과 위험한 링크 scheme을 차단한다. notes 문자열을 그대로 HTML로 삽입하지 않는다.
- HTML에는 로컬 Reveal CSS·JS, 선택한 테마 CSS, Notes 플러그인과 연결 스크립트를 명시적인 순서로 로드한다. 초기화 코드는 외부 JS에 둔다.

### URL과 목차 호환

- 새 목차 링크와 위치 주소는 `#/slide-N` 형식으로 통일하고 Reveal의 hash 기능을 사용한다.
- 기존 `#slide=N` 주소는 초기화 전에 새 형식으로 한 번만 변환한다. 별도의 hash 상태 관리기를 계속 실행하지 않는다.
- 잘못된 번호는 유효한 슬라이드 범위로 보정하고, 해석할 수 없는 주소는 첫 슬라이드로 처리한다.
- 새로고침·직접 링크·목차 이동과 `--no-toc`에서 표지·본문 번호가 어긋나지 않게 한다.

## 5. 테마와 배율

[기본 테마](styles/default.css)를 Reveal DOM과 상태 클래스에 맞춘다.

- Reveal의 핵심 CSS는 항상 로드한다. `--theme`은 그 위에 적용하는 md2ppt 기본 테마를 교체한다.
- CSS 적용 순서는 Reveal 핵심 CSS → 기본 또는 사용자 테마 CSS다.
- 기존 `.stage`의 위치·transform과 `.slide.active`의 표시 제어를 제거하고, 슬라이드 표시와 전체 화면 배율을 Reveal에 맡긴다.
- `.reveal .slides`, `.reveal .slides > section` 등에 범위를 지정해 Reveal 기본 규칙과 본문 layout CSS가 충돌하지 않게 한다.
- 기본 테마의 글자 크기는 슬라이드 좌표계에 맞는 px·em을 기준으로 정리한다. viewport 높이와 자체 stage 배율을 함께 사용하는 계산을 걷어낸다.
- `--stage-width`, `--stage-height`는 기본 1280px·720px로 유지하고, CSS에서 읽은 유효한 픽셀 기준 크기를 Reveal 설정에 연결한다. 테마에 값이 없거나 유효하지 않으면 기본 크기를 사용한다.
- 기존 `--stage-scale`을 이용한 자체 확대·축소를 폐기하고, `--fit-scale`은 콘텐츠 맞춤 용도로 유지한다.
- `section_header`, `title_and_content`, `two_content`, `content_with_caption`, `two_images`와 fallback 그리드를 확인한다.
- 기본 테마의 단일 원본, 사용자 CSS 경로 규칙, 요청 시 재읽기와 수정 후 새로고침 동작을 유지한다.
- 기존 사용자 CSS 중 `.stage`, `.slide.active`, `--stage-scale`에 의존하는 부분은 수정이 필요함을 README에 알리고 새 선택자와 이전 예시를 제공한다.

### 콘텐츠 맞춤과 넘침

Reveal의 화면 배율과 한 슬라이드 안의 콘텐츠 맞춤을 구분한다.

- 기존 콘텐츠 맞춤을 좁은 연결 기능으로 유지한다. stage 전체에 두 번째 scale transform을 적용하지 않는다.
- Reveal `ready`, `slidechanged`, 크기 변경, 이미지 로드와 웹폰트 준비 완료 시 현재 슬라이드를 측정한다.
- 숨겨진 슬라이드의 0 크기를 기준으로 맞춤 값을 계산하지 않는다.
- 콘텐츠가 넘치면 `--fit-scale`을 조절하고, 허용한 축소 범위에서도 넘치면 기존 안내를 표시한다.
- 표지·목차·본문, 이미지가 늦게 로드되는 경우와 발표자 미리보기에서도 같은 배치가 보이게 한다.

## 6. 발표자 화면과 노트

공식 Reveal Notes 플러그인을 이번 전환 범위에 포함한다.

- 공통 slide JSON의 `notes` 배열을 순서대로 렌더링해 해당 슬라이드의 `aside.notes`로 전달한다.
- 노트는 md2ppt에서 안전하게 HTML로 변환하고 `data-markdown`으로 다시 파싱하지 않는다.
- 청중 화면에는 노트를 표시하지 않는다. 발표자 화면에는 현재·다음 슬라이드, 노트와 타이머를 제공한다.
- 노트가 없는 슬라이드에서도 발표자 화면이 열리고 다음 슬라이드를 미리 볼 수 있어야 한다.
- 화면 버튼은 사용자 클릭 안에서 Notes 플러그인의 공개 API에 연결한다. 팝업 차단 시 다시 열 수 있도록 안내한다.
- 청중 화면과 발표자 화면에서 이동한 위치가 동기화되고, 발표 페이지 새로고침 후에도 연결이 복구되는지 확인한다.
- 발표자 미리보기 요청의 query string을 보존하고, receiver 화면에서 보조 UI가 중복 표시되거나 노트 창이 재귀적으로 열리지 않게 한다.

### HTTP 응답과 CSP 조정

현재 [웹 서버](md2ppt/web/server.py)의 CSP는 발표자 화면에 필요한 iframe과 인라인 스크립트를 차단한다. 6.0.2 Notes 플러그인의 실제 동작을 기준으로 다음을 적용한다.

- 발표 페이지의 `frame-src`와 `frame-ancestors`는 같은 origin의 미리보기를 허용하도록 제한한다.
- Notes 플러그인이 팝업에 작성하는 고정 인라인 스크립트에 대해서만 SHA-256 CSP hash를 허용한다. 전역 `script-src 'unsafe-inline'`이나 `unsafe-eval`을 추가하지 않는다.
- 이 hash는 고정한 배포본에서 산출해 리소스 메타정보와 함께 관리하고, 팝업에 상속되는 CSP에서도 실제로 동작하는지 브라우저로 확인한다.
- 기존 이미지 등록 제한, 경로 탐색 차단, MIME 지정과 캐시 방지 규칙을 유지한다.
- 임의의 로컬 HTML·JS 파일을 제공하거나 외부 origin의 iframe을 허용하지 않는다.

## 7. 자체 플레이어 정리

[발표 스크립트](md2ppt/web/assets/player.js)는 Reveal 초기화와 프로젝트 연결 코드로 축소한다.

- 기존 `show()`, 슬라이드 active·inert 관리, 이전·다음 키 처리, stage 배율 계산과 hash 갱신 루프를 제거한다.
- Reveal의 공개 API와 이벤트로 버튼·슬라이드 변경 안내·문서 진단을 연결한다.
- 전체 화면 버튼은 Reveal 발표 영역을 대상으로 브라우저 전체 화면 기능에 연결한다.
- 슬라이드 개수·현재 위치·활성 상태는 Reveal을 기준으로 읽고 별도의 발표 상태를 중복 저장하지 않는다.
- 본문 맞춤과 오류·접근성 안내만 프로젝트 코드로 유지한다.
- [웹 렌더러](md2ppt/web/render.py)와 [기본 테마](styles/default.css)에서도 폐기한 플레이어 전용 DOM·스타일을 정리한다.

## 8. 변경 대상

| 대상 | 작업 |
| --- | --- |
| [Reveal.js 리소스 폴더](md2ppt/web/assets/vendor/reveal/) · 신규 | 고정 버전 배포 파일, LICENSE, 출처·해시·갱신 절차 |
| [웹 렌더러](md2ppt/web/render.py) | Reveal DOM, 슬라이드 ID·목차 링크, 노트, 리소스 로딩 |
| [발표 스크립트](md2ppt/web/assets/player.js) | 자체 엔진을 초기화·연결 코드로 교체 |
| [기본 테마](styles/default.css) | Reveal 상태·배율 규칙에 맞춘 레이아웃과 글자 크기 |
| [웹 서버](md2ppt/web/server.py) | vendor URL 허용 목록, 리소스 사전 확인, CSP와 Notes 미리보기 |
| [패키지 설정](pyproject.toml)·[소스 배포 설정](MANIFEST.in)·[빌드 훅](md2ppt_build.py) | vendor 파일과 기본 CSS의 소스·설치 환경 제공 |
| [웹 검증](tests/test_web.py)·[CLI 검증](tests/test_cli.py) | 새 HTML·노트·리소스·CSP와 기존 옵션 회귀 확인 |
| [README](README.md) | 조작법, 발표자 화면, CSS 이전, 오프라인 실행과 버전 정보 |
| [요구사항](wiki/REQUIREMENT.md)·[결정 기록](wiki/LOG.md) | 전환 범위와 구현 상태 유지 |

공통 Markdown 파이프라인과 PPTX 생성 경로는 재사용한다. 변경이 필요한 경우에도 입력 문법과 slide JSON의 기존 의미를 보존한다.

## 9. 구현 순서

1. [x] 6.0.2 공식 배포 리소스와 LICENSE·해시를 포함하고, 최소 HTML에서 기본 발표와 Notes 팝업의 CSP 동작을 확인했다.
2. [x] vendor 리소스 제공·서버 시작 전 확인·패키징을 연결했다.
3. [x] 렌더러를 Reveal DOM으로 바꾸고 슬라이드 ID·목차·이전 URL 호환을 구현했다.
4. [x] 기본 테마와 콘텐츠 맞춤을 Reveal 배율에 연결하고 기존 자체 발표 상태·이동 코드를 제거했다.
5. [x] 기존 노트를 Notes 플러그인에 연결하고 청중·발표자 화면의 이동·새로고침 동기화를 확인했다.
6. [x] CLI·렌더러·HTTP 회귀 검증, 브라우저 발표 확인과 배포본 설치 확인을 수행했다.
7. [x] README의 사용법과 CSS 이전 안내, 위키와 이 계획의 상태를 구현 결과에 맞춰 갱신했다.

## 10. 검증과 완료 기준

| 구분 | 확인 항목 |
| --- | --- |
| 입력과 렌더링 | embed·한글·공백 경로, 표지·목차·본문, 모든 기존 layout과 fallback, 목록·표·코드·이미지, 빈 슬라이드 보정 |
| HTML·노트 처리 | Reveal가 인식한 슬라이드 수와 공통 JSON의 대응, 노트 순서·서식, raw HTML·위험 링크 차단 |
| HTTP | vendor·기본 CSS·사용자 CSS·등록 이미지의 정상 응답과 MIME, 없는 리소스·경로 탐색의 실패, 잘못된 theme·누락 vendor의 사전 오류 |
| 브라우저 | 버튼·단축키·터치, 전체 화면, overview, 진행 표시·번호, 새 URL·이전 URL·목차·새로고침 |
| 배치와 테마 | 1280×720과 사용자 기준 크기, 창 크기 변경, 기본·사용자 CSS, 긴 표·코드·목차·이미지, 맞춤 후 넘침 안내 |
| 발표자 화면 | 노트 유무, 현재·다음 미리보기와 타이머, 양쪽 화면 이동 동기화·새로고침 복구, 팝업 차단 안내, CSP 오류 없음 |
| 배포·회귀 | wheel·sdist의 JS·CSS·LICENSE·해시 포함, sdist에서 wheel 빌드, 저장소 밖 설치 실행, 기존 PPTX CLI·내장 템플릿·사용자 ref 동작 |

- 기존 테스트를 새 공개 HTML 규칙에 맞게 갱신하고, 노트·리소스 접근·CSP처럼 전환으로 달라지는 경계에 필요한 검증을 추가한다.
- Chromium 계열 브라우저에서 청중 창과 발표자 창을 직접 열어 확인한다. 단순 HTTP 200만으로 발표자 기능 완료를 판단하지 않는다.
- 실제 강의 자료인 “아는 만큼 쓰는 ChatGPT”로 많은 슬라이드와 이미지가 있는 발표를 확인한다. 원본 자료는 수정하지 않는다.
- 설치한 패키지를 저장소 밖에서 실행하고, 네트워크를 끈 상태에서도 로컬 자료의 발표와 발표자 화면이 동작해야 한다.
- 자체 플레이어와 Reveal가 동시에 슬라이드 상태·이동·stage 배율을 관리하는 코드가 남아 있지 않아야 한다.
- 모든 단계와 검증이 끝났을 때 상태를 구현 완료로 바꾼다.

### 구현 결과

- Reveal.js 6.0.2의 공식 배포 JS·CSS·Notes 플러그인과 MIT LICENSE를 고정 SHA-256 메타정보와 함께 포함했다. 서버는 필요한 경로만 제공하고 시작 시 리소스를 확인한다.
- 실제 강의 자료를 브라우저에서 열어 표지·목차·본문 89장을 포함한 91장, 로컬 이미지, 16:9 화면, 컨트롤·단축키·목차 링크·전체 화면·overview·진행 표시·기존 주소 변환을 확인했다.
- 별도 노트 샘플에서 서식 렌더링, raw HTML 이스케이프, 발표자 창의 현재 노트·미리보기와 이동 동기화, 발표 페이지 새로고침 후 복구를 확인했다.
- wheel과 sdist를 만들고 sdist에서 wheel을 다시 빌드했다. 저장소 밖의 설치본에서 기본 발표와 로컬 리소스 로딩을 확인했고 외부 네트워크 요청은 없었다.
- `python -m unittest discover -s tests` 결과 12개 테스트가 통과했다.
- 전환 전용 플레이어 상태·이동 루프와 stage 자체 배율 규칙을 제거하고 `player.js`를 Reveal 초기화·연결 기능으로 축소했다.

## 11. 이번 전환 이후의 범위

자동 파일 감지, 별도 장치와의 원격 발표 동기화, 웹 편집기, 새 Markdown 애니메이션·fragment 문법과 전용 PDF 내보내기 CLI는 후속 작업으로 둔다. Reveal에 내장된 기능을 켜기 위해 기존 입력 문법을 일괄 변경하지 않는다.

## 12. 참고 자료

- [공식 6.0.2 릴리스](https://github.com/hakimel/reveal.js/releases/tag/6.0.2) · [해당 버전 배포 경로](https://github.com/hakimel/reveal.js/blob/6.0.2/package.json)
- [HTML 구조](https://revealjs.com/markup/) · [초기화](https://revealjs.com/initialization/) · [설정](https://revealjs.com/config/)
- [공개 API](https://revealjs.com/api/) · [화면 크기와 배율](https://revealjs.com/presentation-size/) · [테마](https://revealjs.com/themes/)
- [발표자 화면](https://revealjs.com/speaker-view/) · [6.0.2 Notes 플러그인](https://github.com/hakimel/reveal.js/blob/6.0.2/plugin/notes/plugin.js) · [발표자 창 HTML](https://github.com/hakimel/reveal.js/blob/6.0.2/plugin/notes/speaker-view.html)
- [빌드 도구 없는 기본 설치](https://revealjs.com/installation/) · [MIT LICENSE](https://github.com/hakimel/reveal.js/blob/6.0.2/LICENSE)
