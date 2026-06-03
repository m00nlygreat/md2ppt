# Agent Notes

## Packaging Templates

- Built-in PowerPoint templates should live inside the Python project package, not as loose root-level files.
- Include bundled templates as package data, for example `refs/*.pptx` under the package directory.
- Users should not need to know installed package paths. Expose built-in templates by name through CLI options such as `--template default` and `--list-templates`.
- Keep `--ref` for explicit user-provided `.pptx` template paths outside the package.
- If the code is moved under an `md2ppt/` package directory, update the console script entry point to `md2ppt.main:main`.

## 위키 관리

- 이 저장소의 간단한 위키는 [wiki](wiki/)에 둔다.
- 위키 문서는 한국어로 짧고 명확하게 작성한다.
- 위키 문서나 프로젝트 문서를 참조할 때는 백틱 경로 대신 반드시 마크다운 링크와 프로젝트 기준 상대 경로를 사용한다. 예: [요구사항](wiki/REQUIREMENT.md).
- [wiki/REQUIREMENT.md](wiki/REQUIREMENT.md)는 현재 요구사항 요약의 유지본이다. 요구사항을 정리하거나 갱신할 때 이 파일을 함께 관리한다.
- [wiki/LOG.md](wiki/LOG.md)에는 프로젝트 관련 중대 결정사항, 새로 알아낸 사실, 방향 변경을 시간순으로 남긴다.
- 원본 자료 폴더는 사용자가 요청하지 않는 한 수정하지 않는다.
