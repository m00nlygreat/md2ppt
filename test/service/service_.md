---
title: 기획 선배의 맞는 말 대잔치
author: 배문형
---

# 강사 소개

## 강사 소개

- 배문형
	- 인하대학교 영어영문학/문화콘텐츠학 학사
	- 8년차 서비스 기획/프로덕트 오너

### 이력

- '16 ~ '18 : 엘루오씨앤씨
- '18 ~ '19 : 에어코드
- '19 ~ '21 : Fitogether
- '22 ~ '23 : 레피카
- '23 동북권 ICT 이노베이션 스퀘어 강의
- '23 한양대학교 노코드 엔지니어링
- '24 알파코 서비스기획 강의

![](attachments/profile-aigen.png)

# 서비스기획 개론

## 기획이란 무엇인가? 어떻게 공부해야 하나?

### 기획이란 (Planner?)

- Why를 설명하는 것
	- [Lucky Louie - Why?](https://www.youtube.com/watch?v=znE5yuiKj-Y)
	- 기획은 `왜?`로 시작해서 `왜?`로 끝난다.

### 가르칠 수 있는 것인가?

- 기획은 암묵지(Tacit Knowledge)의 영역
	- 강의나 텍스트의 형태로 전달되기 어렵다.
	- 도제식 수련
- 그렇다면 냅다 해보는 수밖에
	- 기획과 역기획
	- 방법론과 도구들
	- 케이스 스터디

![](attachments/ux-then-just-do.png)

## 범기획자 직군들에 대한 소개

### 기술과 패러다임 변화에 의한 직군 다양화

- 웹마스터
- 웹기획자 / 웹 개발자
- 서비스기획자
	- Planner? Designer?
- UI/UX 디자이너
- 프로젝트 매니저
- 프로덕트 디자이너 / 매니저 / 오너 

***

- [기획자가 사라지고 있다](https://seokjun.kim/why-engineers-become-ceo/)
- [개발팀과 개발팀장이 사라져야 하는 이유](https://seokjun.kim/no-reason-for-dev-team/)

## 기획자의 명과 암

- 한국에서는 에이전시에서 자생한 직군이기 때문에, 기획의 담론 자체가 다음에 초점이 맞춰져 있음
	- 고객 대응과 책임소지
	- 제안서와 보고서
	- 있어빌리티

### 기획자라는 이름

- 회사마다 하는 일이 다름
- 어떤 회사들에서는 욕받이 또는 잡부 역할
- 딜레마: 사용자를 위할 것인가? 회사를 위할 것인가?

# 서비스 기획의 Flow

## 더블 다이아몬드 모델

- 기획의 여정은 발산과 수렴을 반복한다.

![](attachments/ux-double-diamond.png)

## 문제 및 요구사항 정의

### 아이디어 도출

- 아이디에이션 (Ideation)
- 이해관계자 인터뷰 (Stakeholder)
	- 이해관계자는 누구나 될 수 있다
	- 같이 일하는 조직, 해당 도메인 종사자
- 문제 정의
	- 어떠한 문제가 있고 이것은 왜 해결되어야 하나?
	- 정의된 문제는 모든 기획의 **최상위 원칙**이 된다.
		- 문제가 하위 기획에 의해 도전을 받고 수정되는 일은 있어도,
		- 하위 기획이 문제를 배반해서는 안됨.

***

### 리서치

- 데스크 리서치 (시장조사)
	- 도메인 영역에 대한 F/U 정도로 충분 (규모, 트렌드 등)
	- 선두와 후발주자들을 자세히 뜯어보고 비교하기
	- 시장 규모 예측
	- 포지셔닝 맵, 경쟁 분석

- 유저
	- 정량적, 정성적 리서치
	- 설문조사, 인터뷰, FGI
	- 기획을 유저에게 떠넘기지 말 것
		- 약은 약사에게, 진료는 의사에게, 기획은 기획자가
		- 유저는 솔직하지 않습니다
	- 가장 열성적이고 협조적인 유저 = 기획자 자신

---

### 솔루션 도출 및 가설 설정

- 문제를 해결하는 직접적인 솔루션
- 가설을 한 문장으로 나타내기!
	- ~~ 한다면 ~~~ 할 것이다!
	- 정량적 지표를 포함하면 좋음
- How Might We? 질문법

***

### 요구사항(User Story) 정의

- 문제를 해결하기 위한 세부 목표
- 유저의 직접적인 욕망을 대표하는 문장의 형태로 작성
	- `I, as a ~~~ want to ~~~~ so that ~~~~`
- 또는 일상 언어로 제품 내의 유저 행동을 표현해도 좋다

## 기능 및 화면 정의

### 기능 정의

- 기능은 요구사항에 대한 실질적 해답
- CRUD를 고려하면서 작성하기

### 화면 정의

- 화면 ⊃ 기능
	- 그러나 기능과 화면의 하이어라키는 다르다.
	- 카드 소팅, IA
- 플로우 차트, 와이어프레임, 프로토타입

## 구현 및 테스트

![](attachments/프로그램의%20완성%20과정.png)

---

### 테스트

- 테스트 케이스
	- ID, 기능명, 화면, 환경, 재현경로, 
- 블랙박스 테스트
- 화이트박스 테스트
	- 커버리지(Coverage)
		- 구문(Statement): 전체 프로그램의 실행 완료를 검증
		- 분기(Branch): 모든 분기를 한 번씩 실행한다
		- 경로(Path): 각 조건마다 한 번씩 참/거짓을 수행하며 검증
		- 조건(Condition): All True/All False 케이스를 검증

![](attachments/ux-test-case.png)

## 유지보수 및 고도화

- 고도화 과정은 모든 디자인 프로세스를 상황에 맞게 축소하여 진행한다. 즉 미니 프로덕트를 만드는 것이라고 볼 수 있음
	- 버그 수정
	- 리팩토링
	- 리뉴얼
	- 기능 추가

### UX 고도화

- A/B 테스팅
- 유저 행동 데이터 분석

# 기획자의 무기

## 소프트 스킬

### 호기심

- the one must-have skill

### 커뮤니케이션

- 이해와 공감
- 논리력
- 솔직하고 투명한 커뮤니케이션

***

### 꼼꼼함

- MECE 하게 정리하기
	- Mutually Exclusive, Collectively Exhaustive
	- 상호배타적이며 전체 포괄적
- 일반적인 의미의 꼼꼼함 역시 필수

---

### 창의력

- 본질과 형식
	- 본질은 형식의 상위 호환
	- 형식을 따르는 사람은 창조가 불가능
	- [반도체 전설 짐 켈러](https://www.youtube.com/watch?v=iwXr1IRaqWA)
- 기싸움을 하지 말자
	- [모욕적인 질문에 답하는 스티브 잡스](https://www.youtube.com/watch?v=Ew53EGl0rXo)
	- [유튜버에게 생각지도 못한 질문을 들은 일론 머스크](https://www.youtube.com/watch?v=WY73exaVpyw)
	- [People that are really good](https://www.youtube.com/watch?v=tkHvxLwLx3M)

***

### 그리고 약간의 고집

- Think Different!
- 똑똑한 사람은 쉽게 예민해지기 마련입니다.
	- 하지만 당신이 예민하다는 사실이 당신의 똑똑함을 증명하지는 않습니다.

## 하드스킬

### 글쓰기

- 구조적 글쓰기
	- 마크다운
	- 세컨드브레인
- 생각을 표현하기도 하고, 정리를 할 때도 쓸 수 있는 도구
- 적어도 주어와 술어가 호응하는 글을 쓸 수 있도록

### 말하기

- 명료하고 전달력 있는 목소리
- 이해와 공감을 전할 수 있는 some kinda 연기력
	- 솔직함은 훈련해야 하는 것입니다.

***

### 툴 사용

- 생각을 표현하거나 정보를 구축하는 다양한 도구 활용
	- 오피스, 피그마, 생성형 AI
	- 데이터 분석
	- 동영상 편집, 촬영
	- 노코드 도구: 노션, 웹 빌더, 자동화 등

---

### 데이터 분석

- 데이터를 정량적, 정성적으로 분석하고 인사이트를 도출할 수 있는 능력
	- 데이터 분석은 어디까지나 도구일 뿐
	- 반드시 가설 검증의 형태로 이뤄져야 한다.

***

### 개발과 기술에 대한 이해

- [오늘도 개발자가 안 된다고 말했다](https://www.yes24.com/Product/Goods/97919905)
- 그럴 거면 그냥 개발 공부하는 게 낫지 않을까?

## 라이브러리

#### 다양한 지식과 경험의 독자적 체계

### 경험

- 일상 속에서도 불편함을 발견하기
- 적극적으로 눈 앞의 문제들을 해결하기
- 경험으로부터 귀납적 원리를 이끌어 내기
- 다양한 프로젝트 경험

***

### 지식

- Every knowdledge in the world counts.
	- 특히 기술과 컴퓨터에 관한 지식
	- 도메인 날리지(Domain Knowledge)
- 특히 어떤 기술을 내가 안다. 라고 말할 수 있다는 것은
	- 그 기술과 관련된 전후 역사를 알고 있다는 것
- 나만의 지식 체계를 구축하기
	- 블로그
	- 세컨드 브레인

---

### 용어

- 나의 언어로 재해석해야 내 것이 됨.
- 정확한 용어에 집착하지 말고 **뭣이중헌지**를 판단하기

### 방법론 (Frameworks)

- 그 어떤 것도 본질에 선행하지 않음
- 방법론은 도구로써 활용할 때 가치가 있으며, 방법론에 매몰되어서는 안됨
	- 그것이 방법론의 본질이기도 하고
- 방법론/프레임워크는 모든 문제상황을 해결하는 전가의 보도가 아니므로 
	- 반드시 나의 맥락과 사정을 분석하여 적합한지 판단해야 하고
	- 이것이 가능하면 방법론을 그대로 따르는 것이 아니라 알맞게 각색하여 수용할 수 있으며
	- 나아가서는 자신만의 방법론을 만들어낼 수 있기 때문

---

### 우상 숭배 금지

- 애자일
- 디자인 시스템
- REST API
- 디자인 패턴
- 방법론, UX 도구들
- 데이터분석

#### 비판적으로 사고할 것!

![](attachments/rest.png)

## 마크다운(Markdown)

- HTML의 Subset인, 리치 텍스트를 표현하기 위한 간이 문법
- 이름은 HTML(Hypertext Markup Language)의 말장난
- [마크다운 가이드](https://m00nlygreat.notion.site/ba2a279ebbf94484b4bdfa42105935a0)

### 플레인 텍스트와 리치 텍스트

- 플레인 텍스트: 메모장
- 리치 텍스트: 워드패드

### 사용처

- 디스코드, 슬랙, 노션, Github
- Obsidian, LogSeq, Github, ChatGPT, StackEdit, Joplin

![](attachments/markdown-preview.png)

---

![](attachments/markdown-example.png)

## 마크다운의 문법 소개

*제목*

```markdown
＃ 제목
＃＃ 제목 2
＃＃＃ 제목 3
```

*텍스트*

```markdown
**굵게**
*이탤릭*
~~취소선~~
```

***

*인용*

```markdown
> 인용
```

*리스트*

```markdown
- 순서 없는 리스트 항목
- 순서 없는 리스트 항목

1. 순서 있는 리스트 항목
2. 순서 있는 리스트 항목
```

---

*코드*

````markdown
```
코드 블록
```
````

*링크*

```markdown
[링크 텍스트](URL)
```

*이미지*

```markdown
![대체 텍스트](URL)
```

***

*수평선*

```markdown
ㅡㅡㅡ
```

*테이블*

```markdown
| 헤더1 | 헤더2 |
|------|------|
| 셀1   | 셀2   |
```

*체크박스*

```markdown
- [x] 완료 항목
- [ ] 미완료 항목
```

## Markdown is the new MS Word

1. 마크다운은 생각과 아이디어를 **최소한의 서식으로 보존하고 정리**하는 데에 도움을 줍니다.
2. 마크다운은 여러 포맷으로 변환될 수 있습니다. 따라서 레이아웃이나 서식과 같은 장치보다도 **원본 콘텐츠를 지키고 더욱 개선하는 일**에 적당합니다.
3. 마크다운은 글의 구조를 표현하는 데에 필요한 모든 규칙을 가지고 있습니다. 따라서 **구조적 글쓰기 훈련**을 하는 데에도 도움이 됩니다.
4. ChatGPT와 같은 대부분의 거대언어모델 역시 마크다운 호환 형식으로 답변하며, 마크다운을 읽고 쓰는 데에 능숙합니다. 말하자면 AI와 대화할 때도 최적화되어 있는 것이죠.
5. 마크다운은 점차 더 많은 현세대 애플리케이션에 통합되고 있습니다. 곧 더 많은 곳에서 마크다운을 보게 될 것입니다.

## 옵시디언 (Obsidian)

- 마크다운과 노트의 연결을 근간으로 하는 개인 지식 DB 구축 도구
	- 제텔카스텐(Zettelkasten), 세컨드브레인
- RAG를 통해 생성형 AI와 내 지식 데이터베이스를 사용한 챗봇 구축
- 지식의 연결을 시각화하는 Graph View

![](노코드%20엔지니어링/attachments/obsidian-graph.gif)

## Mermaid.js

- 마크다운을 채택한 많은 에디터에서 호환되는 다이어그램/차트 작성 도구
- 간단한 플레인 텍스트 문법으로 차트 또는 다이어그램 작성
- [Mermaid.js Live Editor](https://mermaid.live/edit)

```markdown
> GPT등의 언어모델은 스스로는 다이어그램을 그리지 못하지만 mermaid.js 문법의 코드를 작성할 수 있다!
```

![](modules/attachments/mermaid-example.png)

# 프로젝트 매니지먼트

## 소프트웨어 개발 조직의 성격

- 전통적, 한국적 방법: 여러 문서와 워터폴 방식을 따르는 조직
- 스타트업, 해외 유래: 프로토타입과 TDD 위주의 애자일 조직

![](attachments/Pasted%20image%2020240711154412.png)

## 애자일과 워터폴

- [애자일 소프트웨어 선언](https://agilemanifesto.org/iso/ko/manifesto.html)
- 빠른 주기로 프로덕트의 개발을 반복하며 테스트 주도(Test-driven)형으로 완성품의 품질을 높여가는 소프트웨어 개발 방식
	- 유저를 내팽개치지 않음

![](attachments/그게%20워터폴.png)

---

![](attachments/Pasted%20image%2020240711113304.png)

## 린 스타트업

- MVP를 위주로 빠르게 가설을 검증하고 피봇(Pivot)을 통해 Product-Market Fit을 찾아가는 창업 프레임워크
- Build -> Measure -> Learn의 구성을 따름
- [프로그래밍 좀비님의 이야기](https://www.youtube.com/watch?v=XYR2-_H4PzI)

![](서비스기획/attachments/Pasted%20image%2020241121025646.png)

---

### MVP

- Minimum Viable Product, 최소 기능 제품
- 문제를 해결하는 최소한의 제품 구성
- 프리토타입(Pretotype)
	- "**Fake it** till you make it"
	- [유의미한 실패는 성공의 어머니, 프리토타입](https://blog.wishket.com/유의미한-실패는-성공의-어머니-프리토타입pretotype/)

### 피봇(Pivot)

- MVP 등의 실험으로부터 얻어진 것을 통해 인사이트를 도출하고 제품 또는 문제, 타겟 등을 수정하여 새로운 전략을 도출하는 것

---

![](attachments/uxdesign05.png)

## 스크럼

- 애자일의 실질적인 수행방법으로 스프린트를 반복해가며 프로덕트를 개발한다. 

### 스프린트 (Sprints) 

- 실질적인 스크럼의 단위. 주로 1-2주 또는 4주 정도의 스프린트를 반복하며 프로덕트 개발
	- 스프린트 설계
	- 스프린트 수행
	- 스프린트 회고

### Jira와 Kanban

![](attachments/Pasted%20image%2020240712222211.png)

## 간트차트와 업무 분해도(WBS)

![](attachments/Pasted%20image%2020241118034608.png)


# UI/UX 개론

## 소프트웨어를 분류하는 여러가지 방법

### 플랫폼에 의한 분류

- 네이티브
- 크로스플랫폼
	- 웹 (브라우저)
	- 자바 (가상머신)
- 하이브리드

***

### 시스템 레이어에 의한 분류

- 운영체제 (Operating System)
- 드라이버 (Drivers): 주변기기(Peripherals)를 이용하기 위한 소프트웨어
- 미들웨어 (Middlewares)
- 응용 프로그램 (Applications)

---

### 사용 목적에 따른 분류

- 오락용
- 사무용
- 교육용
- 산업용

### 공급 방법에 의한 분류

- B2B 소프트웨어
- B2C 소프트웨어

***

### 네트워크 상의 역할에 따른 분류

- 서버
	- 웹 (Web servers)
	- 애플리케이션 백엔드
	- 데이터베이스
- 클라이언트

### 의존도에 따른 분류

- 스탠드얼론(Standalone)
- Integrated
	- 의존성(Dependancy)

---

### 구축 형태에 따른 분류

- 클라우드
	- Saas (Software as a service)
- 온프레미스 (On-premise)

### 저작권에 따른 분류

- 오픈소스 (자유 소프트웨어)
- 클로즈드 소스 (또는 사유Proprietary 소프트웨어)

## 직관

- 直觀, Intuition
- 보고 아는 것

![](attachments/Pasted%20image%2020240711032041.png)

---

### 직관의 우선순위

1. 내가 아는 것
2. 내가 아는 것과 닮은 것
3. 모르지만 왠지 알겠는 것
4. 논리적으로 알아챌 수 있는 것

![](attachments/Pasted%20image%2020240711120701.png)

## 어포던스

### Affordance

- 제임스 깁슨
- 행위자와 환경 사이의 관계에 존재하는 행동 가능성(possibility of action)
- 행위자가 인지하든 하지 않든, 어포던스는 존재함

![](attachments/Pasted%20image%2020241118035957.png)

---
### 지각된 어포던스 (Perceived Affordance)

- 또는 기표(Signifiant), 도널드 노먼
- 사회적/개인적 경험에 의해 만들어질 수 있음
- 의도적으로 설계되거나 우연히 만들어질 수도 있음

- [어포던스 - 위키백과](https://ko.wikipedia.org/wiki/%EC%96%B4%ED%8F%AC%EB%8D%98%EC%8A%A4)

***

### 어포던스의 응용

- 이미지들의 선택과 허용가능한 상호 작용 양쪽에서 일반적인 사용법을 따르라.
- 원하는 행동을 묘사하는 단어를 사용하라. 예를 들어 마우스로 클릭가능한 링크가 연결된 그래픽 오브젝트에 여기를 클릭라고 표시하는 것.
- 메타포(Metaphor, 은유)를 사용하라.
- 인터페이스를 학습한 이후 이것을 다른 부분에 활용할 수 있도록 지속적으로 같은 컨셉 모델을 따르도록 하라.

# 인터랙션: 조작과 피드백

## 인터랙션(Interactions)

![](attachments/uxdesign04.png)

## 장치(Devices)

### 입력 장치 (Input Devices)

- 키보드
- 마우스
- 센서
	- 마이크
	- 카메라
		- 심박수 측정?
	- 조도 센서
	- 가속도계
	- 자이로스코프
	- 근접 센서
	- LiDAR (Light Detection And Ranging)
- 펜
	- 디지타이저 태블릿
- 게임 패드

***

#### 스마트폰은 가히 센서 혁명이라고 볼 수 있다.

---

### 출력 장치 (Output Devices)

#### 피드백과 정보 조회를 위한 장치들

- 디스플레이
- 스피커
- 진동 모듈
	- 탭틱 엔진
	- HD 진동
	- 스피커로도 쓴다..?

***

### 입출력 동시

- 터치스크린
	- 3D 터치
- VR 헤드셋
- 어댑티브 트리거 (게임 패드)

---

### 기타

- 통신 모듈
	- 셀룰러
		- 3G, 4G(LTE), 5G
	- WI-FI
	- 블루투스
	- NFC
	- UWB
	- 이더넷

## 주요 인터페이스

### 키보드

- 컴퓨터의 시작과 함께 했던, 아마도 영원 불멸의 인터페이스
	- 펑션 키: 맥에는 없다
	- 방향키
		- **포커스**를 옮길 때 사용
	- 모디파이어 키: Ctrl, Alt, Win / Cmd, Option, Ctrl
	- 엔터/리턴, Esc, Space Bar, Backspace, Tab
	- 누르기, 길게 누르기

### 마우스

- 포인팅 디바이스, 2차원 평면 상의 좌표를 가리키는 도구.
	- 상대 좌표
	- Left, Right, Middle, Mouse4, 5
	- 포인팅, 호버, 클릭, 더블 클릭, 클릭 앤 드래그, 클릭 앤 홀드

***

### 터치스크린

- 21세기의 인터페이스
	- 입력과 출력이 동시에 이뤄짐
	- 인터랙션이 가능한 UI 요소의 최소 현실 크기 `10mm × 10mm`
	- 탭, 탭 앤 홀드＝롱 프레스, 더블 탭, 스와이프, 플릭, 핀치, 3D 터치, 멀티 핑거 제스처

# 유저 인터페이스, UI

## UI를 뜯어보는 기준

- Looks: 어떻게 생겼는지
	- Status: 어떤 상태를 가지는지
- Interact: 어떤 인터랙션을 가지는지
- Data: 어떤 데이터가 암시되어 있는지

![](attachments/uxdesign03.png)

# Primitives

## Button

#### Looks

- 누를 수 있는 사각형의 영역과 버튼의 기능을 설명하는 레이블
	- 간혹 아이콘을 포함하기도
- Hover, Pressed(Active)
- 공통: Enabled/Disabled, Focused/Focused not, Empty/Filled, Validated, not Validated

#### Interact

- Activate
	- 누르기
	- 떼기

***

#### Data

- onClick : function()

---

![](attachments/Pasted%20image%2020240711122706.png)

## Radio Button

### Looks

- 눌렀을 때 속이 채워지는 동그란 버튼과 레이블
	- 이것이 여러 개 있음
- Checked, Checked not

### Interact

- Activate

### Data

- items: Item[]
- selected: Item

![](attachments/Pasted%20image%2020240711131815.png)

## Checkbox

### Looks

- 빈 사각형에 체크마크, 그리고 레이블
- Checked, Checked not, (Indeterminate)

### Interact

 - Activate, Deactivate

### Data

- checked: boolean

![](attachments/Pasted%20image%2020240711132444.png)

## Switch

### Looks

- 현실세계의 on/off 스위치를 본따, 핸들이 있고 핸들의 가동 범위 안에서 on/off의 영역이 있음
- Activated / Deactivated

### Interact

- Activate, Deactivate

### Data

- activated: boolean

![](attachments/Pasted%20image%2020240711132750.png)

## Input

### Looks

- 사각형의 입력 영역, Placeholder, Title, Cursor, (Icon), (alert)
- Empty, Filled, Error, Accepted

### Interact

- Activate
- Enter
- Validate

### 모바일에서

- [인풋 입력 시 적절한 키보드가 나와야 한다.](http://mobileinputtypes.com/)

![](attachments/Pasted%20image%2020240711133227.png)

## Slider

- 핸들과 핸들의 1차원 가동범위. 스텝 눈금
	- Range Variant
- 스텝(Steps)
- 스크롤바도 일종의 슬라이더?

### Interact

- Set

### Data

- value: number

#### 난 슬라이더가 싫어요

![](attachments/Pasted%20image%2020240711150048.png)

## Progresss bar

### Looks

- 진행상태를 나타내는 막대
- 보통 전체를 현재 진행이 채우는 형태로 작성
- Completed / In Progress / Stuck

### Interact

- 끝나기를 기다리며 하염없이 쳐다보기

### Data

- value: 0<number<=1
	- .. 인데 이 number 계산을 어떻게 하느냐가 중요

![](attachments/Pasted%20image%2020240711150334.png)

## Dropdown ≒ Selectbox, Combobox

### Looks

- 누름틀과 누르면 열리는 리스트
- Open / not open

### Interact

- Click to open
- Set

### Data

- items: Item[]
- selected: Item

![](attachments/Pasted%20image%2020240711151934.png)

# Composites

## Form

- 특정 목적의 데이터들을 입력받는 인풋들의 집합 (예: 회원가입)

![](attachments/Pasted%20image%2020240711135853.png)

## Tab

- 여러 페이지들을 묶어 버튼으로 전환할 수 있도록 추상화한 컨테이너 요소

![](attachments/uxdesign01.png)

## Dialog

- 대화상자. 

![](attachments/Pasted%20image%2020240711140919.png)

## Modal ≒ Window

- 현재 맥락과 구분되는 특정한 목적을 가지고 실행되는 독립된 작은 창
- 실행시 부모 컨테이너의 Interaction 중단됨 ≠ Modeless
- Pop-ups / Pop-over

![](attachments/Pasted%20image%2020240711141425.png)


## Screen / Page

- 페이지의 구분과 논리적 위계는 자의적임
- 왼쪽 -> 오른쪽
	- 이전 -> 이후
	- 큰 것 -> 작은 것
	- Public -> Private
- 유저가 길을 잃지 않게 하기
	- 논리적인 위계
	- Breadcrumbs
	- One Page One Thing
	- Single Column
	- 카드소팅(Card Sorting)

![](attachments/Pasted%20image%2020240711151605.png)

## List

- 여러 개의 항목을 보여주는 컨테이너
- Swipe actions

![](attachments/Pasted%20image%2020240711162442.png)

---

### 다양한 기기에서의 List

![](attachments/Pasted%20image%2020240711162607.png)

---

## Card

- 프로퍼티를 가진 복수 개의 복잡한 정보를 나타내는 효과적인 UI 요소
- Flat UI의 핵심

![](attachments/Pasted%20image%2020240711162808.png)

## Popup / Context Menu

- 우클릭하면 나타나는 상황에 맞는 (Contextual) 메뉴
- Dropdown과 비슷하게 메뉴 출현 위치에 대해 고민 필요

![](attachments/Pasted%20image%2020240711163523.png)

## 기타

- Splash Screen
- Accordion
- Focus
- Icon
- Carousel
- Dashboard
- Navigation Bar / Top App Bar
- Tab Bar / Navigation Bar
- Notification Bar
- Stepper / Spinner

***

- Toast
- Banner
- Popper
	- Popover
- Tooltip
- Bottom Sheet
	- Grabber
- Floating Action Button
- CTA Button
- Skeleton
- Sticky Header

## 왠진 모르겠지만 음식 이름으로 부름

- Hamburger
- Kebob
- Bento
- Toast
- Breadcrumbs

![](attachments/Pasted%20image%2020240711121345.png)

## 이름에 집착하지 맙시다

- UI 요소, 인터랙션의 정확한 이름은 찾기도 어렵고 **팀원 간 합의도 어려움**
- 따라서 혼자 정확한 이름을 쓰는 고집을 부렸을 때의 이득은 그냥 '멋있어 보인다'뿐.
- 중요한 것은 팀 내에서의 소통입니다

# UI 기타

## UX 바이블

- 구글 [Material Design Guide](https://m3.material.io/)
- 애플 [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [닐슨 노먼 그룹](https://www.nngroup.com/)
- [Funny Worst Input Fields](https://www.boredpanda.com/funny-worst-input-fields/)

## 디자인 시스템

### Atomic Designs

![](attachments/Pasted%20image%2020240711164257.png)

---

- [SOCAR FRAME](https://design.socar.kr/)
- [Wanted Design Library](https://www.figma.com/community/file/1355516515676178246)
- [Gmarket Design System](https://gds.gmarket.co.kr/)
- [신한은행 SOLID Design System](http://jlworks.cool/html/work_solid.html)
- [LINE Design System](https://designsystem.line.me/)
- [11번가 Design System](https://design.11stcorp.com/)
- [리디 디자인 시스템](https://www.makerhz.me/d3ad0b6f-3698-4907-9bcd-0372db8fd4a8)
- [디지털정부 UI/UX 가이드라인](https://uiux.egovframe.go.kr/guide/index.html)

---

## 디자인 트렌드

- 스큐어모픽 Skeuomporphic
- 플랫 Flat
	- 플랫 2.0
- 뉴모피즘 Neumorphism
	- 글래스모피즘 Glassmorphism
- 네오 브루탈리즘 Neo Brutalism

# UX 도구 - 설문조사

## 설문조사

- 가장 효율적이고 많은 가능성을 내포한 사용자 리서치 도구
- 비용과 시간이 적게 들면서도 다양한 의견을 수집할 수 있음

### 단점과 한계

- 단방향 소통의 한계로 커뮤니케이션 장애 발생 가능
	- 설문자의 명예와 신뢰에도 타격을 줄 수 있음
- 원하는 결과를 얻으려면 아주 섬세한 안배가 필요
- 답변자에게 진지함을 기대하기 어렵기에 심도 있는 인사이트를 얻기 어려움

## 설문조사의 방법과 도구

- 폼 도구
	- 구글 폼
	- 타입폼, Tally.so, 왈라
	- Notion Forms
	- 대면 설문조사
- 분석 도구
	- 스프레드시트
	- 데이터 분석 도구 (파이썬 등)

***

### 방법

- 설문조사 **목적 및 가설** 설정
- 설문조사 설계 
- 설문조사 배포
- 결과 수집 및 분석

## 설문조사는 남을 귀찮게 하는 일

- 기본적으로 답변자는 설문조사에 참여해야하는 이유가 없고
- 거의 전적으로 설문조사는 답변자의 선의에 기대야 하는 일
	- 그렇기 때문에 오히려 주의깊게 수행해야

### 신뢰감 얻기

- 신원과 목적을 확실히 밝힐 것
- 정중하고 예의바른 태도

### 사례

- 작게나마 사례하기
	- 보상이 큰 경우 체리피커 개입 주의
- 사례를 위한 전화번호 등 수집 시 개인정보 보호법 준수
	- 동의 항목 첨부

***

### 최소한 보람이라도 있어야

- 답변자가 답변을 하면서 이걸 대체 어디다 쓸 수 있을까? 라는 의문이 들면 설문조사는 가치가 없어짐
- 목적과 의의를 확실히 제시하되, 의도는 숨겨야 좋은 답변을 얻을 수 있음
- 답변자도 설문 결과가 궁금하다!

## 가설설정

- 별다른 목적 없이 데스크 리서치의 일환으로써 설문조사를 이용할 수 있으나, 활용도가 떨어짐
- 따라서 반드시 목적과 가설을 뚜렷하게 설정할 필요 있음.

### 가설이 없는 설문결과로는 보고서에 파이차트 밖에 그릴 수 없다.

- 고작 이 정도 목적으로 설문조사에 기꺼이 참여하는 답변자들의 성의를 이용해도 될까?

## 설계

### 설문조사 또한 일종의 제품

- 인사이트를 얻을 수 있는 **양질의 답변**을 **최대한 많이** 얻는 것을 목적으로 하는 제품
	- 설문조사는 단방향 소통이므로
	- 질문이 명확히 이해되고 답변을 내기 위해 너무 많은 노력이 들지 않도록 신중하고 섬세한 질문 작성
- 답변자(유저)에 대한 이해를 기반으로 제출까지 이탈하지 않도록 섬세하게 설계

***

### 설문에도 UX가 필요

- 답변 맥락과 사정에 맞게끔 설문경험을 최적화하기 위해 설문 경로를 분기처리합니다.
- 그 외 폼 도구들의 기능을 최대한 활용
	- Default answer
	- 필수/비필수 질문 구분
	- 히든 필드, URL 파라미터
	- 이미지나 미디어를 적극적으로 활용

---

### 명확한 대상이 없는 경우 모든 사람을 위해 만들 것

- 답변 대상자를 좁힐 수 없는 경우, 모든 사람을 위한 경로(선택지)를 설계해야 합니다.
- 그게 아니라면 설문의 서두에 대상자를 명확히 밝혀 전혀 관계가 없는 사람이 설문을 시작하는 것을 막아야 합니다.

### 불쾌하게 하지 말 것

- 계급, 성별, 종교, 정치 등 민감한 주제를 질문하는 경우 신중할 것
- 개인적인 주제를 다룰 때 보안에 대한 고려를 철저히 할 것
- 필수 항목은 보수적으로 선택

---

### 답변할 수 있는 질문인가?

- [리처드 파인만 "자석이 서로 밀어내는 이유"](https://www.youtube.com/watch?v=3smc7jbUPiE)

![](attachments/Pasted%20image%2020241119153654.png)

---

### 약은 약사에게, 진료는 의사에게, 기획은 기획자가

- 유저에게 문제에 대한 답(기획)을 요구하지 말 것.
	- '어떤~ 기능이 있으면 좋을 것 같으세요?'
	- '\~\~\~한 기능이 있으면 구매 의향이 있으세요?'

- 기본적으로 설문조사에 참여하는 답변자는
	- 선의로 참여하고 있기에 긍정적 피드백을 줄 가능성이 높음
	- 또는 진짜 눈 앞의 선택을 하는 상황이 아니기에 진지하지 않을 가능성이 높음
	- 혹은 자기 자신의 진짜 욕망에 대해 이해하지 못하고 있을 가능성이 높음

***

- 따라서 설문자는 오로지 퍼실리테이터(Facilitator)의 역할로서 상황을 상상하게 만들거나 추상적이고 해석의 여지가 있는 질문을 통해 답변자의 본의를 이끌어내는 데에 집중해야 한다.
	- 미로 속의 생쥐를 정점 타격하는 것이 아니라 주변부를 타격, 경로를 차단하며 막다른 길로 몰아가는 감각으로

## 배포

- 설문조사는 배포된 이후에는 수정할 수 없습니다.
	- 데이터 정합성의 문제

### 배포채널

- 설문조사를 배포한 채널과 규모에 대해 간략히 기록하여 해당 채널이 어떤 편향이 있는지 체크
	- '30대 직장인 단톡방'
	- '운동 동호회 네이버 밴드' 등 
- 필요한 경우 URL 파라미터와 히든 필드 같은 폼 도구의 기능을 사용하여 대신할 수 있음

## 분석

![](attachments/Pasted%20image%2020241118191933.png)

# UX 도구 - 유저 퍼소나

## 유저 퍼소나 User Persona

- 전체 사용자 집단을 여러 특질을 기준으로 클러스터링했을 때 해당 군집의 사용자를 대표하는 구체화된 가상의 유저

### 데이터를 근거로 할 것

- 데이터에 기반하지 않은 유저 퍼소나는 아무런 의미가 없다
- 다양한 속성(Attributes)에 근거한 사용자 특질(Characteristics) 발견
	- 인구통계학적(Demographics)
		- 연령, 성별, 지역, 교육수준
	- 사이코그래픽스(Psyhographics, 가치관, 심리적 특성)
		- 가치관, 믿음, 관심사, 라이프스타일
	- 행동 특성(Behavioral Traits)
		- 사용빈도, 브랜드 충성도, 사용자 의견 제시

***

### 퍼소나 속성의 활용

다양한 퍼소나의 속성을 다음과 같은 측면의 UX 의사결정에 활용할 수 있다.

- 인구통계학적 속성
	- 개인화된 콘텐츠, 문화적 민감성, 접근성 측면
- 사이코 그래픽스 속성
	- 제품 선호도, 의사결정, 정서적 연결 측면
- 행동 특성 속성
	- 개인화된 추천 기능, 기능 최적화, 온보딩과 재방문 전략

---

![](attachments/Pasted%20image%2020241118204819.png)

---

![](attachments/Pasted%20image%2020241118204856.png)

# UX 도구 - 사용자 여정 지도

## 사용자 여정 지도 (User Journey Map)

- 사용자가 특정 시나리오에서 제품을 접하고 이용하는 과정에서 욕망과 감정이 어떻게 변화하는지를 나타내는 지도
	- 고객이 제품을 알게 되고 이용하고, 떠나는 모든 과정을 한 눈에 볼 수 있도록 하여
	- 우리가 개선할 부분, 신경써야 할 부분, 미처 놓치고 있는 부분을 파악할 수 있도록 함
- 머릿속에 있는 것과 눈 앞에 펼쳐져 있는 것은 몰입과 체감 차원에서 다름
- 여정 지도는 제품과 함께 살아있으며, 계속 업데이트되어야 함

***

### 요소

- 주인공 (Actor)
- 시나리오
- 목표 (Goal)
- 단계 (Phase)
- 감정 (Emotion)
- 페인 포인트
- 터치 포인트: 고객과 제품이 접하는 지점

---

![](attachments/ux-journey-map.png)

---

![](attachments/ux-journey-map-2.png)

# 기타 UX 도구들


## 어피니티 다이어그램

- 스타트업 하면 떠오르는 이미지 속에 반드시 있는 그거
- 불규칙한 정성적 데이터를 분류하고 의미있는 데이터로 만드는 방법

![](attachments/ux-affinity-diagram.png)

## 플로우차트 (Flowchart)

- 흐름도. 로직을 표현하는 다이어그램
- 본래는 코딩을 위한 알고리즘 프로토타이핑의 용도이므로 플로우차트의 기호들은 컴퓨터의 동작과 관련되어 있다
- 흐름도의 주체가 무엇인지를 엄격하게 고려하면서 작성하기

![](attachments/ux-flow-chart.png)

## 휴리스틱 (Heuristic)

- **발견법**(發見法). 불충분한 시간이나 정보로 인하여 합리적인 판단을 할 수 없거나, 체계적이면서 합리적인 판단이 굳이 필요하지 않은 상황에서 사람들이 빠르게 사용할 수 있게 보다 용이하게 구성된 간편추론의 방법
	- 즉 **어림짐작**

### 휴리스틱의 여러 이름

- 간편법, 간편추론법, 어림법, 어림셈, 어림짐작법, 주먹구구법, 편의법, 쉬운 발견법, 판단 효과, 발견법, 경험적 지식, 즉흥적 추론, 쉬운 방법, 지름길

***

###  뻔히 눈에 보이는 것을 추론하기 위해 애쓸 필요는 없다

- 기획자의 직관을 이용해 의사결정 및 판단을 빠르게 할 수 있지만 그만큼 주관성에 빠져버릴 위험이 있다.
- 그러나 시행착오를 통해 개선되는 만큼, 휴리스틱은 암묵지를 획득하기 좋은 훈련법이기도 하다.

## A/B 테스트

- 동일한 조건의 사용자 여럿에 서로 다른 버전의 애플리케이션을 제공하고 유저의 행동을 관찰하는 UX 테스트 기법

### 주의

- 너무 자주 많이 하지 말 것. 기본적으로 리스크가 전제됨
- A/B 테스트 결과는 절대적이거나 항구적이지 않다
- 지역최적점에 머물게 될 위험

![](attachments/Pasted%20image%2020241119032229.png)

## UX 히트맵

- 스크롤, 클릭, 커서 움직임 등의 유저 행동을 누적된 히트맵으로 보기
- 사용자의 정보 습득 경로와 주 의사결정 요인 등을 확인할 수 있는 지표

![](attachments/Pasted%20image%2020241119033057.png)

## 카드소팅 (Card Sorting)

- 주로 화면의 순서와 메뉴의 하이어라키를 결정하기 위해
- 사용자에게 아이템을 카드의 형태로 쥐어주고 알아서 배치해보게 하는 방법
- 사용자가 익숙하고 직관적이라고 느끼는 화면의 순서, 메뉴의 배치를 알아낼 수 있다

![](서비스기획/attachments/ux-card-sorting.png)

# UX 이모저모

## 다양한 사용자를 고려하기

### IT 취약계층

- 시니어, 어린이 등 IT 기기 사용이 익숙치 않은 사용자
- 더욱 더 친근한 용어와 단순한 화면을 사용
	- 모션을 적극적으로 사용할 것
- 현실의 메타포를 사용하거나 입력장치 조작을 단순화하는 등의 노력 필요
- 시니어를 대상으로 할 경우 텍스트 크기를 크게

### 외국인

- 섬세한 번역 필요.
	- 간혹 1:1 번역이 적합하지 않은 경우가 있음
		- 이 경우 UI, 코드레벨에서 다국적 언어 지원에 관한 Variation이 필요할 수도 
- 각 나라의 문화와 관습에 맞는 UX 설계가 필요함과 동시에
- 국내 문화가 다른 나라에 비해 특이한 점에 대해서도 주의해야

***

### 제품을 '일'로서 사용하게 되는 사람들

- 직관성보다는 편리함 우선
	- 어차피 배워서 쓰는 것이고, 사용 빈도가 높기 때문에 조작이 간편한 것이 중심
- 단축키, 개인화 등 업무적 사용에 있어서의 배려 필요

### 장애인

 - 스크린리더를 사용하는 시각 장애인
	 - UI의 논리적 구조(Hierarchy) 엄격하게 준수
	 - 대체 텍스트 등 접근성 항목
 - 소리를 들을 수 없는 청각 장애인
	 - 진동 등의 대체 피드백
	 - 자막 지원

## UX Writing

- UX의 큰 축을 담당하는 프로덕트의 텍스트를 좀 더 사용자 경험에 걸맞게 작성하려는 노력

### UX at its finest

- UX 라이팅은 궁극의 UX로, 가장 섬세하고 디테일한 UX설계의 끝이라고 볼 수 있다
- 사용자의 문제를 해결하는 동시에, 제작자들의 이익을 위한 장치이기도 함
- 사용자에게 복잡한 작업을 수행하게 할 때 특히 중요
- 제품의 전체 Tone of Voice를 담당하며 브랜드의 퍼스낼러티를 구축

### 결국은 좋은 글쓰기와 진정성 있는 태도의 문제

---

## 실전 UX 라이팅

### 참고자료

- [신한카드 UX Writing 가이드북](attachments/신한카드%20UX%20Writing%20가이드북_v1.0.pdf)
- [WWDC24 UX 라이팅으로 앱에 개성 더하기](https://developer.apple.com/kr/videos/play/wwdc2024/10140/)

## 넛지 이론, Nudge Theory

- 팔꿈치로 쿡쿡 찌르다. 라는 의미의 영단어로 **자유주의적 개입 또는 간섭**을 의미
- 행동을 유도하는 대표적인 방법으로 인센티브와 벌칙(당근과 채찍)이 있다면
- 넛지는 은연 중에 작은 신호들이나 의도적인 혼란으로 행동을 유도하는 방법
- 과하면 다크 패턴이 된다. 

![](attachments/ux-nudge-fly.png)

## 다크 패턴

- 사용자에게 손해, 그리고 서비스에 이익이 되도록 의도적으로 UX를 배치하는 것.

***

### 해리 브리그널의 12 Dark Patterns

1. 속임수 질문(Trick Questions)
2. 소매넣기(Sneak into Basket), 2014년부터 EU에서 불법
3. 싸구려 호텔(Roach Motel), 가입은 쉽게 해지는 어렵게
4. 개인정보 주커링(Privacy Zuckering)
5. 가격비교 차단(Privacy Comparison Prevention)
6. 주의집중 분산(Misdirection)
7. 숨겨진 가격(Hidden Cost)
8. 미끼와 스위치(Bait and Switch), 숨겨진 버튼
9. 호혜적 선택강요(Confirmshaming)
10. 위장된 광고(Disguised Ads), 콘텐츠로 위장한 광고
11. 강제 연속 결제(Forced Continuity), EU불법
12. 친구로 위장한 스팸(Friend Spam)

---

![](attachments/Pasted%20image%2020241119053358.png)

---

![](attachments/Pasted%20image%2020241119053735.png)

---

![](attachments/uxdesign06.png)

---

### 콜린 그레이의 5 Dark Patterns

1. 잔소리형(Nagging)
2. 경로방해형(Obstruction)
3. 인터페이스 간섭(Interface Interference)
	- Checked by default
	- Next 버튼 시차
4. 은닉형(Sneaking)
5. 행동강제형(Forced Action)

---

![](attachments/ux-dark-pattern.png)

## Thumbzone

- 모바일 애플리케이션의 설계 시 한 손으로 기기를 파지했을 때 UI 요소에 접근하기 위한 엄지손가락의 가동 범위
- 되도록 Thumbzone 안에 자주 사용하는 기능을 배치할 것이 요구됨

![](attachments/ux-thumbzone.png)

## 3-Click Rule

- 애플리케이션의 모든 기능에 접근하는 데 3번의 클릭을 넘으면 안된다.
	- 라는 주장을 했던 **2001년의 UX 미신**
- 비슷하게 최상위 메뉴가 7개 이하여야 한다라는 미신도 있다.

![](attachments/ux-3-click-rule.png)

## 예쁜 웹사이트는 왜 전환에 실패하는가

- [Why Beautiful Websites Don't Convert](https://www.youtube.com/watch?v=Toonu-cTE60)

![](attachments/ux-why-beautiful-websites-dont-convert.png)

## 10 Laws of UX

[10 Laws of UX](https://brunch.co.kr/@sower/167)

- 제이콥의 법칙: 다수가 사용하는 인터페이스를 제공해라
- 피츠의 법칙: 사람들은 크고 가까운 것을 선택하는 경향이 있다.
- 힉의 법칙: 선택지가 많아지면 선택에 걸리는 시간은 (로그함수의 형태로) 늘어난다.
- 밀러의 법칙: 사람들이 한 번에 기억할 수 있는 건 7(±2)개 정도의 요소뿐이다.
- 포스텔의 법칙: 사용자의 행동(입력)은 너그럽게 수용하되, 입력을 요구하는 건 제한하라.

***

- 피크엔드 법칙: 사람들은 절정과 마지막 순간만을 기억한다.
- 심미적 사용성: 예쁘면 사람들은 사용성이 좋다고 생각한다.
- 폰 레스토프 효과: 비슷한 사물이 여러 개 있으면 그 중 색다른 것만 기억한다.
- 테슬러의 법칙: 시스템의 복잡성은 어느 한도 이상으로 축소할 수 없다.
- 도허티 임계: 사람들의 생산성을 증대시키는 인터랙션의 속도는 0.4초 이하이다.

## One thing per page

- 한 화면에는 유저가 한 번에 소화시킬 수 있는 만큼의 정보량(One thing)을 제공해야 한다.
- 토스가 좋아하는 UX 원칙
- [거꾸로 입력하는 가입 화면](https://toss.tech/article/toss-signup-process)
- [토스 디자이너들의 프로덕트 원칙](https://brunch.co.kr/@figmaster/8)

![](attachments/ux-onething-per-page.png)

## System-wide preferences

- 유저의 시각적 선호도 등을 시스템에서 설정하고, 애플리케이션이 이를 따르도록 하는 트렌드
	- 다크모드, 텍스트 스케일 등
- 시스템의 특정 조건(시간 등)이나 다양한 사용자 선호에 따라 맞춤 설정을 이용할 수 있음

![](서비스기획/attachments/ux-toss-dark-mode.png)