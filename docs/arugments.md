# 파이프라인 인수 작성 규칙

- `-i`,  `--input` {filepath}: 입력 파일 경로
  - 혹은 python dictionary를 args로 받기
- `-o`, `--output` {filepath}: 출력 파일 이름
  - 혹은 python dictionary를 리턴

## 디폴트

- md2json: {filename}.json
- json2slide: {filename}.slides.json
- json2pptx: {filename}.pptx
