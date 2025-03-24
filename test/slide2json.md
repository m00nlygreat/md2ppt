# 백서: json2slide 변환 규칙

## 1. 개요

- **md2json.py**는 마크다운 파일을 분석해 YAML frontmatter와 본문을 파싱하여,\
  **frontmatter**와 **tokens** 구조를 갖춘 JSON을 출력합니다.
- **json2slide.py**는 **md2json.py**의 출력을 받아, **슬라이드(및 placeholder) 구조를 갖춘 JSON**으로 재구성합니다.
  - 최종적으로 이 JSON은 **python-pptx**를 이용해 PPT 파일을 생성할 때 사용합니다.

---

## 2. 데이터 흐름

1. **Markdown 파일** → (md2json.py) → **1차 JSON**\
   (마크다운 토큰들이 담긴 JSON: frontmatter + tokens)

2. **1차 JSON** → (json2slide.py) → **2차 JSON**\
   (슬라이드 및 placeholder 구조로 가공된 JSON)

3. **2차 JSON** → (python-pptx) → **PPT 파일**\
   (실제로 PowerPoint 문서를 생성)

---

## 3. md2json.py가 제공하는 JSON 예시

```json
{
  "frontmatter": {
    "title": "My Document",
    "author": "Alice",
    "date": "2025-03-16"
  },
  "tokens": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "children": [
        { "type": "text", "raw": "GPT 개요" }
      ]
    },
    {
      "type": "paragraph",
      "children": [
        { "type": "text", "raw": "GPT는 자연어 처리 모델입니다." }
      ]
    },
    {
      "type": "wildcard_break"
    }
  ]
}
```

### 3.1 frontmatter

- 문서의 메타정보를 포함 (title, author, date 등).

### 3.2 tokens

- 본문을 마크다운 단위별로 토큰화한 리스트.
- 주요 **type**:
  - **heading**: `level`로 H1\~H6 구분.
  - **paragraph**: 일반 텍스트 단락.
  - **list**: 순서 있는/없는 목록.
  - **wildcard\_break**: 슬라이드 내 컬럼(placeholder) 구분 용도.
  - **thematic\_break**: 슬라이드 구분 용도(또는 필요에 따라 다른 해석 가능).
  - **comment\_block**: 주석(`key`, `value` 쌍). 주로 layout 정보를 강제 지정하기 위해 사용.
  - **image**: 이미지 삽입용.
  - **quote**: 인용문.
  - **code**: 코드 블록.
  - **table**: 표.
  - ...

---

## 4. json2slide.py의 출력 구조 (최종 JSON)

### 4.1 슬라이드 구조

```json
{
  "slides": [
    {
      "title": "슬라이드 제목",
      "layout": "title_content",
      "placeholders": [
        {
          "type": "text",
          "content": [
            {
              "runs": [
                { "text": "이것은 일반 텍스트입니다." },
                { "text": "굵게", "bold": true },
                { "text": " 표시된 텍스트입니다." }
              ]
            }
          ]
        },
        {
          "type": "image",
          "src": "attachments/example.png"
        }
      ]
    }
  ]
}
```

#### 슬라이드 객체의 주요 필드

1. **title**: 슬라이드 제목
   - 실제 PPT 변환 시 \*\*placeholder[0]\*\*로 매핑될 수 있음.
2. **layout**: 슬라이드 레이아웃(예: `"title_content"`, `"two_columns"`, `"cover"` 등)
   - **comment\_block**에서 `layout`이 지정된 경우 우선 적용.
   - 지정이 없으면 자동 판단 가능.
3. **placeholders**: 슬라이드 내 콘텐츠를 담는 ‘구획’들
   - `wildcard_break`를 만나면 **새로운 placeholder** 생성.
   - placeholder 배열 안에 **텍스트, 이미지, 테이블, 차트 등**이 들어갈 수 있음.

---

### 4.2 Placeholder 구조

```json
{
  "type": "text",
  "content": [
    {
      "runs": [
        { "text": "Hello" },
        { "text": "World", "italic": true }
      ]
    }
  ]
}
```

혹은

```json
{
  "type": "image",
  "src": "attachments/example.png"
}
```

혹은

```json
{
  "type": "table",
  "rows": [
    ["헤더1", "헤더2"],
    ["데이터1", "데이터2"]
  ]
}
```

#### placeholder의 주요 속성

1. **type**
   - `"text"`: 일반 문장이나 리스트 등을 하나의 텍스트 단위로 처리.
   - `"image"`: 이미지.
   - `"table"`: 표.
   - `"code"`: 코드 블록.
   - `"quote"`: 인용문.
   - `"chart"`: (차트가 있을 경우)
   - `"list"`: 리스트를 별도 type으로 둘 수도 있음.
2. **content** (혹은 `rows`, `src` 등)
   - `"text"`인 경우: `content` 안에 run 단위 텍스트.
   - `"image"`인 경우: `src`에 이미지 경로.
   - `"table"`인 경우: `rows`로 2차원 배열.
   - `"code"`인 경우: `monospace: true`와 함께 텍스트 runs를 처리.

---

## 5. 텍스트 스타일(run) 구조

**python-pptx**에서 텍스트 스타일은 **run 단위**로 적용하므로,\
JSON에서도 **run 단위**로 스타일을 지정한다.

| 속성          | 의미                                       |
| ----------- | ---------------------------------------- |
| `bold`      | `true`면 굵게 표시 (굵은 글꼴)                    |
| `italic`    | `true`면 이탤릭(기울임꼴) 적용                     |
| `underline` | `true`면 밑줄                               |
| `monospace` | `true`면 고정폭 글꼴 (코드 블록 등)                 |
| `text`      | 실제 텍스트 내용                                |
| `hyperlink` | `{"address": "http://..."}` 등으로 하이퍼링크 표시 |

예시:

```json
"runs": [
  { "text": "이것은 " },
  { "text": "강조된", "bold": true },
  { "text": " 텍스트입니다.", "italic": true, "hyperlink": { "address": "http://example.com" } }
]
```

---

## 6. 슬라이드 분리 규칙

1. ``: 새로운 슬라이드 시작
2. `` (`---` / `___`): 새로운 슬라이드 시작 (옵션)
3. ``: 간지(섹션 표지)로서 독립 슬라이드 (프로젝트 요구사항에 따라)

예시 규칙이며, 프로젝트 정책에 따라 바뀔 수 있음.

---

## 7. placeholder 분리 규칙 (`wildcard_break`)

- `` (`***` 등)가 등장하면, **현재 슬라이드 내에서 새로운 placeholder**를 생성.
- 즉, 한 슬라이드 안에서 구획을 나눌 때 사용.
  - 예: 두-세 개의 컬럼, 혹은 다른 구역 등.

---

## 8. comment\_block과 layout 지정

- `` 형태 예시

  ```json
  {
    "type": "comment_block",
    "key": "layout",
    "value": "custom_layout",
    "raw": "[layout]: # (custom_layout)"
  }
  ```

- **슬라이드 레이아웃 결정**:

  1. 슬라이드에 해당하는 **tokens** 중 `comment_block`에서 `"key" == "layout"`이 있으면 `"value"` 값을 **layout으로 강제 지정**.
  2. 없으면 **자동 판단**(또는 별도의 로직)으로 layout 결정.
     - 예: `wildcard_break` 포함 시 `"two_columns"`.
     - 텍스트+이미지 혼합이면 `"image_with_text"`.
     - 이미지만 있으면 `"image_only"`.
     - 등등.

---

## 9. 예시: 종합 변환 사례

### 9.1 입력 (md2json.py 결과)

```json
{
  "frontmatter": {
    "title": "My Document",
    "author": "Alice"
  },
  "tokens": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "children": [{ "type": "text", "raw": "GPT 개요" }]
    },
    {
      "type": "comment_block",
      "key": "layout",
      "value": "cover"
    },
    {
      "type": "paragraph",
      "children": [{ "type": "text", "raw": "GPT는 자연어 처리 모델입니다." }]
    },
    {
      "type": "wildcard_break"
    },
    {
      "type": "paragraph",
      "children": [{ "type": "text", "raw": "이것은 새 placeholder에 들어갑니다." }]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "children": [{ "type": "text", "raw": "다음 슬라이드" }]
    },
    {
      "type": "paragraph",
      "children": [
        { "type": "strong", "children": [{ "type": "text", "raw": "굵은" }] },
        { "type": "text", "raw": " 텍스트입니다." }
      ]
    }
  ]
}
```

### 9.2 최종 변환 (json2slide.py 결과)

```json
{
  "slides": [
    {
      "title": "GPT 개요",
      "layout": "cover",
      "placeholders": [
        {
          "type": "text",
          "content": [
            {
              "runs": [
                { "text": "GPT는 자연어 처리 모델입니다." }
              ]
            }
          ]
        },
        {
          "type": "text",
          "content": [
            {
              "runs": [
                { "text": "이것은 새 placeholder에 들어갑니다." }
              ]
            }
          ]
        }
      ]
    },
    {
      "title": "다음 슬라이드",
      "layout": "title_content",
      "placeholders": [
        {
          "type": "text",
          "content": [
            {
              "runs": [
                { "text": "굵은", "bold": true },
                { "text": " 텍스트입니다." }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- 첫 번째 슬라이드: `comment_block`(layout: cover)에 따라 **layout이 cover**로 지정.
- `wildcard_break`로 인해 **placeholders**가 2개 존재.
- 두 번째 슬라이드: `heading level 2`로 인해 새 슬라이드 시작, layout은 `"title_content"`(자동 판단).
- `paragraph` 내 `strong`이 `bold: true`로 변환됨.

---

## 10. 구현 시 주의사항

1. **빈 슬라이드** 방지

   - 슬라이드가 시작되었는데 콘텐츠가 하나도 없는 경우는 무시하거나 조정.

2. **빈 placeholder** 방지

   - `wildcard_break`가 연속으로 나와 placeholder만 생성되고 아무 내용이 없을 경우는 무시할 수 있음.

3. **들여쓰기 리스트(depth)**, **코드 블록**, **인용문(quote)** 등 세부적인 토큰 변환

   - 모든 텍스트는 결국 `runs` 형태로 변환하여 스타일(bold, italic, monospace 등)을 설정.

4. **이미지, 표, 차트** 등은 python-pptx 함수로 변환 시 주의

   - `add_picture`, `add_table`, `add_chart` 등을 사용.
   - JSON 구조에서는 `type": "image"`, `type": "table"`, `type": "chart"`로 구분.

5. **comment\_block**의 다른 `key`가 나올 수도 있음

   - 예: `[notes]: # (Slide note...)` → 슬라이드 노트에 활용 가능.

6. **title과 0번 placeholder**

   - 실제 PPT 변환 시 `title`을 0번 placeholder로 매핑해도 됨.
   - JSON 상에서는 가독성을 위해 `title` 필드를 분리해두는 것이 합리적.

---

## 11. 레이아웃 결정 (추가 규칙)

아래 규칙에 따라 **슬라이드 변환이 끝난 후** placeholder의 개수와 미디어 구성요소를 분석하여 최종 `layout` 값을 설정할 수 있습니다. 만약 `comment_block`에 의해 layout이 이미 지정되어 있으면 그 값을 우선 사용합니다.

1. **Heading 1(H1)을 만난 경우** → `layout = "section_header"`

   - 섹션 표지(간지) 역할을 하는 슬라이드.

2. **텍스트와 다른 미디어(차트, 이미지, 테이블 등)가 있는 경우** → `layout = "content_with_caption"`

   - 텍스트 일부와 미디어가 함께 존재하여 설명/캡션이 필요한 경우.

3. **placeholder가 2개인 경우** → `layout = "two_content"`

   - 예: `wildcard_break`로 인해 정확히 두 구역으로 분할된 경우.

4. **title과 하나의 placeholder만 있는 경우** → `layout = "title_and_content"`

   - 일반적인 단일 본문 PPT.

### 레이아웃 우선순위 예시

- **H1 발견 시**: 해당 슬라이드는 무조건 `section_header`로.
- **이미 layout이 comment\_block으로 지정**되었다면 → 해당 layout 사용.
- placeholder 개수 2개라면 → `two_content`.
- 텍스트+미디어 혼합이라면 → `content_with_caption`.
- 그 외(placeholder 1개) → `title_and_content`.

---

## 맺음말

이 백서는 **마크다운에서 JSON**을 거쳐 **PPT**로 변환하기 위해 필요한 **json2slide.py** 규칙을 총망라했습니다.

- **슬라이드 구분** (H2, thematic\_break)
- **placeholder 구분** (wildcard\_break)
- **텍스트 스타일** (run 단위)
- **이미지, 표, 차트 등 비텍스트 요소** 처리
- **comment\_block**을 통한 layout 강제 지정
- **최종 레이아웃 결정** (section\_header / content\_with\_caption / two\_content / title\_and\_content 등)

이 규칙을 기반으로 구현하면,

```
Markdown → md2json.py → (중간 JSON) → json2slide.py → (슬라이드 JSON) → python-pptx → PPT
```

라는 파이프라인이 안정적으로 동작하게 될 것입니다.

추가적인 세부 사항(예: 색상, 폰트 크기, 레이아웃 템플릿 등)은 **python-pptx** 구현 단계에서 자유롭게 커스터마이징 가능합니다.

이상으로 **json2slide.py** 변환 규칙 백서를 마치겠습니다.

