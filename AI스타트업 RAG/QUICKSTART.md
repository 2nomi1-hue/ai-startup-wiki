# 🚀 빠른 시작 가이드 (Quick Start)

**5분 안에 AI Startup RAG Chatbot을 실행하세요!**

## 📋 필수 준비물

- Python 3.8+ 설치됨
- OpenAI API Key 보유 ([https://openai.com/api](https://openai.com/api))

## ⚡ 3단계 설치

### 1️⃣ 환경 설정 (2분)

```bash
# 가상 환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2️⃣ 의존성 설치 (2분)

```bash
pip install -r requirements.txt
```

### 3️⃣ 환경 변수 설정 (1분)

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하고 API Key 추가
# OPENAI_API_KEY=sk-your-api-key-here
```

## 🎯 실행하기

### 옵션 A: 웹 인터페이스와 함께 (권장)

```bash
python app.py
```

**브라우저에서 열기:** http://localhost:5000

### 옵션 B: RAG 시스템만 테스트

```bash
python rag_chatbot.py
```

### 옵션 C: Docker 사용

```bash
docker-compose up
```

## 💬 사용해보기

### 웹 인터페이스
1. http://localhost:5000 열기
2. 질문 입력:
   - "What is an AI startup?"
   - "Tell me about machine learning"
   - "How should I build an AI product?"

### API 사용

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is an AI startup?"}'
```

## 📚 다음 단계

1. **문서 추가**
   ```bash
   # knowledge_base/ 폴더에 .md, .txt, .pdf 파일 추가
   cp your_notes/*.md knowledge_base/raw/
   
   # 벡터 스토어 재구성
   curl -X POST http://localhost:5000/api/rebuild
   ```

2. **자세한 가이드 읽기**
   - README.md - 전체 문서
   - SETUP_GUIDE.md - 상세 설정 가이드

3. **배포하기**
   - Docker로 컨테이너화
   - 클라우드에 배포 (AWS, Google Cloud, Heroku 등)

## 🐛 문제 해결

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key not found"
.env 파일에 API Key 확인

### "Port 5000 already in use"
```bash
PORT=5001 python app.py
```

### "No documents found"
1. `knowledge_base/` 폴더 확인
2. 문서 추가 후 재부팅

## 📖 문서 구조

```
AI스타트업 RAG/
├── app.py                 # 웹 애플리케이션
├── rag_chatbot.py        # RAG 시스템
├── requirements.txt      # 의존성
├── README.md            # 전체 가이드
├── SETUP_GUIDE.md       # 상세 설정
├── QUICKSTART.md        # 이 파일
├── .env.example         # 환경 변수 템플릿
├── Dockerfile           # Docker 설정
├── docker-compose.yml   # Docker Compose
└── knowledge_base/      # 과정 자료
    ├── raw/             # 강의 노트
    ├── wiki/            # 개념 문서
    └── index.md         # 마스터 인덱스
```

## 🔗 유용한 리소스

- **OpenAI API 문서:** https://platform.openai.com/docs
- **LangChain 문서:** https://python.langchain.com
- **Chroma 벡터 DB:** https://www.trychroma.com

## 🎓 예제 질문들

```
"AI 스타트업의 성공 요소는?"
"머신러닝이란 무엇입니까?"
"데이터는 왜 중요한가?"
"AI 제품을 개발하는 방법은?"
"RAG가 무엇입니까?"
```

## ✅ 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] OpenAI API Key 보유
- [ ] 가상 환경 활성화
- [ ] requirements.txt 설치됨
- [ ] .env 파일 생성 및 API Key 추가
- [ ] app.py 실행
- [ ] http://localhost:5000 접속 확인
- [ ] 질문 입력 및 답변 받음
- [ ] README.md 읽음

## 🚨 주의사항

⚠️ **OpenAI API Key 보안:**
- 절대 git commit에 포함하지 않기
- .env 파일을 .gitignore에 추가
- 공개 저장소에 업로드하지 않기
- 정기적으로 Key 로테이션

---

**축하합니다! 이제 AI Startup RAG Chatbot이 실행 중입니다! 🎉**

더 자세한 정보는 README.md와 SETUP_GUIDE.md를 참고하세요.
