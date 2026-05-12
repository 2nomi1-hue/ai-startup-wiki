# 📋 AI Startup RAG Chatbot - Setup Guide

이 가이드는 AI Startup RAG Chatbot을 설정하고 실행하는 방법을 단계별로 설명합니다.

## 1️⃣ 사전 요구사항 확인

### 필수 항목
- **Python 3.8+** - [Python 다운로드](https://www.python.org/downloads/)
- **pip** - Python과 함께 설치됨
- **OpenAI API 계정** - [https://openai.com/api](https://openai.com/api)
  - ChatGPT API 액세스 필요
  - API Key 준비

### 선택 사항 (Docker 사용 시)
- **Docker** - [Docker 다운로드](https://www.docker.com/products/docker-desktop)
- **Docker Compose** - Docker Desktop에 포함

---

## 2️⃣ 프로젝트 설정

### 단계 1: 파일 구조 확인

프로젝트 폴더에 다음 파일들이 있는지 확인하세요:

```
AI스타트업 RAG/
├── app.py                    # Flask 웹 애플리케이션
├── rag_chatbot.py           # RAG 시스템 코어
├── requirements.txt         # Python 의존성
├── README.md                # 주 설명서
├── SETUP_GUIDE.md          # 이 파일
├── .env.example            # 환경 변수 템플릿
├── Dockerfile              # Docker 설정
├── docker-compose.yml      # Docker Compose 설정
├── templates/
│   └── index.html         # 웹 UI
└── knowledge_base/        # 과정 자료 (수동으로 추가)
    ├── raw/               # RAW 노트
    ├── wiki/              # Wiki 문서
    └── index.md           # 마스터 인덱스
```

### 단계 2: Python 가상 환경 생성

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 단계 3: 의존성 설치

```bash
pip install -r requirements.txt
```

설치 시간: 약 2-5분

---

## 3️⃣ OpenAI API 설정

### 단계 1: API Key 획득

1. [OpenAI 웹사이트](https://platform.openai.com/account/api-keys) 방문
2. "Create new secret key" 클릭
3. API Key 복사 (다시 보이지 않으므로 안전한 곳에 저장)

### 단계 2: 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env
```

`.env` 파일을 편집하고 API Key 추가:

```env
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-3.5-turbo
KNOWLEDGE_DIR=./knowledge_base
CHROMA_DB_DIR=./chroma_db
DEBUG=False
PORT=5000
```

---

## 4️⃣ 지식 기반 (Knowledge Base) 설정

### 디렉토리 구조 생성

```bash
mkdir -p knowledge_base/raw
mkdir -p knowledge_base/wiki
```

### 문서 추가

#### 옵션 A: 샘플 데이터 사용 (테스트용)

먼저 샘플 데이터로 테스트할 수 있습니다. 추가 설정이 필요 없습니다.

```bash
python app.py
# 자동으로 샘플 데이터 로드
```

#### 옵션 B: 자신의 문서 추가

1. **RAW 노트 추가**
   ```bash
   # knowledge_base/raw/ 에 .md, .txt, .pdf 파일 추가
   cp /path/to/lecture_notes/*.md knowledge_base/raw/
   ```

2. **Wiki 문서 추가**
   ```bash
   # knowledge_base/wiki/ 에 문서 추가
   cp /path/to/wiki_docs/*.md knowledge_base/wiki/
   ```

3. **마스터 인덱스 생성**
   ```bash
   # knowledge_base/index.md 생성
   ```

### 문서 형식 예시

**knowledge_base/raw/lecture_01.md:**
```markdown
# AI Startup Lecture 01: Introduction

## Topics Covered
- What is an AI Startup?
- Market Overview
- Key Success Factors

## Key Points
1. AI startups focus on technology
2. Data is the new currency
3. Speed to market matters
```

**knowledge_base/wiki/glossary.md:**
```markdown
# Glossary

## RAG
Retrieval Augmented Generation - AI 시스템이 문서 기반에서 정보를 찾아 답변 생성

## LLM
Large Language Model - 대규모 언어 모델 (예: GPT-4)
```

---

## 5️⃣ 애플리케이션 실행

### 옵션 A: 로컬 Python 실행 (권장)

```bash
# 1. 가상 환경 활성화
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 2. 애플리케이션 실행
python app.py
```

**출력:**
```
🚀 Starting AI Startup RAG Chatbot on port 5000
 * Running on http://0.0.0.0:5000
```

**브라우저에서 열기:** http://localhost:5000

### 옵션 B: Gunicorn으로 실행 (프로덕션 유사)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 옵션 C: Docker로 실행

```bash
# Docker 이미지 빌드
docker build -t ai-startup-rag .

# 컨테이너 실행
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-your-key \
  -v $(pwd)/knowledge_base:/app/knowledge_base \
  ai-startup-rag
```

### 옵션 D: Docker Compose 사용 (권장)

```bash
# 1. .env 파일 작성 (위에서 설정함)

# 2. 실행
docker-compose up

# 3. 중지
docker-compose down
```

---

## 6️⃣ 애플리케이션 사용

### 웹 인터페이스

1. 브라우저에서 **http://localhost:5000** 열기
2. 질문 입력 예시:
   - "AI 스타트업이란 무엇인가?"
   - "머신러닝의 기초를 설명해주세요"
   - "AI 제품을 만드는 방법은?"

### API 직접 사용

```bash
# 채팅 요청
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is an AI startup?"}'

# 건강 상태 확인
curl http://localhost:5000/api/health

# 시스템 통계
curl http://localhost:5000/api/stats
```

### 벡터 스토어 재구성

새 문서 추가 후 벡터 스토어 업데이트:

```bash
# 방법 1: API 사용
curl -X POST http://localhost:5000/api/rebuild

# 방법 2: Python 코드
python -c "from rag_chatbot import AIStartupRAG; rag = AIStartupRAG(); rag.build_vectorstore()"
```

---

## 7️⃣ RAG 시스템만 테스트

웹 인터페이스 없이 RAG 시스템 테스트:

```bash
python rag_chatbot.py
```

**출력 예시:**
```
Loading RAG system...
✅ Loaded 3 documents
✅ Created 15 document chunks
✅ Vector store created and saved to ./chroma_db

==================================================
Testing RAG Chatbot
==================================================

❓ Question: What are the key characteristics of an AI startup?
✅ Answer: An AI startup is a company that uses artificial intelligence...
📚 Sources:
   - AI Startup Fundamentals
```

---

## 8️⃣ 트러블슈팅

### 문제: "OpenAI API Key not found"

**해결책:**
```bash
# .env 파일 확인
cat .env

# 또는 환경 변수 직접 설정
export OPENAI_API_KEY=sk-your-key
```

### 문제: "No documents found"

**해결책:**
```bash
# 문서 확인
ls -la knowledge_base/
ls -la knowledge_base/raw/

# 문서 추가 후 재구성
python -c "from rag_chatbot import AIStartupRAG; rag = AIStartupRAG(); rag.build_vectorstore()"
```

### 문제: Port 5000 이미 사용 중

**해결책:**
```bash
# 다른 포트 사용
PORT=5001 python app.py
```

### 문제: "ModuleNotFoundError: No module named 'langchain'"

**해결책:**
```bash
# 의존성 재설치
pip install -r requirements.txt

# 또는 특정 모듈 설치
pip install langchain openai chromadb
```

### 문제: Docker 빌드 실패

**해결책:**
```bash
# Docker 캐시 제거
docker system prune -a

# 다시 빌드
docker build -t ai-startup-rag .
```

---

## 9️⃣ 성능 최적화

### 메모리 사용 줄이기
```python
# rag_chatbot.py에서
chunk_size=500,  # 기본값 1000에서 감소
chunk_overlap=100  # 기본값 200에서 감소
```

### 응답 속도 향상
```python
# 검색 문서 수 감소
retriever=self.vectorstore.as_retriever(
    search_kwargs={"k": 2}  # 기본값 3에서 감소
)
```

### 비용 절감
```bash
# gpt-3.5-turbo 사용 (더 저렴)
MODEL_NAME=gpt-3.5-turbo

# 대신 gpt-4 사용 가능하면:
MODEL_NAME=gpt-4
```

---

## 🔟 다음 단계

### 1. 문서 추가
- 강의 노트를 `knowledge_base/` 에 추가
- 벡터 스토어 재구성

### 2. 사용자 인터페이스 커스터마이징
- `templates/index.html` 수정
- 브랜드 색상/로고 변경

### 3. 클라우드 배포
- [AWS 배포 가이드](README.md#aws-deployment)
- [Google Cloud Run 배포](README.md#google-cloud-run)
- [Heroku 배포](README.md#heroku)

### 4. 모니터링 추가
- 로그 수집 (Sentry, DataDog)
- API 사용량 추적
- 성능 메트릭

---

## 📞 지원

문제가 있으면:

1. **README.md** 의 troubleshooting 섹션 확인
2. **에러 메시지** 검색
3. **OpenAI API 상태** 확인: https://status.openai.com
4. **LangChain 문서**: https://python.langchain.com

---

## 안보 주의사항 ⚠️

- ✅ `.env` 파일을 `.gitignore` 에 추가
- ✅ API Key를 공개하지 않기
- ✅ Production에서는 `DEBUG=False` 설정
- ✅ 정기적으로 API 액세스 로그 확인
- ✅ 사용자 입력 검증 (SQL Injection 방지)

---

**축하합니다! AI Startup RAG Chatbot 설정이 완료되었습니다! 🎉**

Questions? 이 가이드를 다시 참고하거나 README.md를 확인하세요.
