# 🔵 Google Cloud만으로 배포하기 (GitHub 없음)

GitHub 계정 없이 **Google Cloud Run만 사용**하여 RAG 챗봇을 배포합니다.

---

## 🎯 이 가이드의 장점

✅ GitHub 계정 불필요  
✅ 간단한 설정  
✅ 거의 무료 (월 200만 요청까지)  
✅ 확장성 우수  
✅ Google 생태계 통합  

---

## 📋 사전 준비

1. **Google Cloud 계정** (gmail.com으로 무료 생성)
2. **OpenAI API 키** (sk-로 시작)
3. **gcloud CLI** (로컬에서 배포용)
4. **Docker** (로컬에서 이미지 테스트용)

---

## 1️⃣ Google Cloud 계정 설정 (10분)

### 1.1 Google Cloud 계정 생성

1. **[Google Cloud Console](https://console.cloud.google.com)** 방문
2. **"Google Cloud에 오신 것을 환영합니다"** → **무료로 시작하기**
3. Google 계정으로 로그인 (또는 새로 생성)
4. 결제 정보 입력 (크레딧 카드, 후불 방식)
   - **중요:** 월 $200 무료 크레딧 제공
   - 초과 사용 시에만 청구

### 1.2 새 프로젝트 생성

1. **프로젝트 선택** (좌상단)
2. **새 프로젝트** 클릭
3. 프로젝트 이름 입력: `ai-startup-rag`
4. **만들기** 클릭 (약 1분 소요)

### 1.3 필수 API 활성화

프로젝트 생성 후:

1. **상단 검색 창** → `cloud run api` 검색
2. **Cloud Run API** 클릭
3. **활성화** 버튼 클릭

다시 검색:

1. **Artifact Registry API** 검색 및 활성화
2. **Cloud Build API** 검색 및 활성화

**확인:**
```
✅ Cloud Run API
✅ Artifact Registry API
✅ Cloud Build API
```

---

## 2️⃣로컬 환경 설정 (15분)

### 2.1 Google Cloud SDK 설치

#### Windows
1. **[Google Cloud SDK 다운로드](https://cloud.google.com/sdk/docs/install-components?hl=ko)** 방문
2. **Windows용 설치** 클릭
3. 설치 마법사 따라하기
4. PowerShell/CMD 재시작

#### macOS
```bash
# Homebrew 사용 (권장)
brew install --cask google-cloud-sdk

# 또는 직접 설치
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### Linux
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2.2 gcloud 초기화

```bash
# 1. gcloud CLI 로그인
gcloud auth login

# 브라우저가 열리면 Google 계정으로 로그인

# 2. 프로젝트 설정
gcloud config set project ai-startup-rag

# 3. 기본 지역 설정 (필수)
gcloud config set run/region us-central1

# 4. 확인
gcloud config list
```

**출력 예시:**
```
[core]
project = ai-startup-rag
region = us-central1

[run]
region = us-central1
```

### 2.3 Docker 설치 (선택)

로컬에서 테스트하려면:

```bash
# macOS (Homebrew)
brew install --cask docker

# Windows
# https://www.docker.com/products/docker-desktop 다운로드

# Linux
sudo apt-get install docker.io
```

---

## 3️⃣ 프로젝트 준비 (5분)

### 3.1 필요한 파일 확인

이미 생성된 파일들:

```
AI스타트업 RAG/
├── app.py                    ✅ (필수)
├── rag_chatbot.py           ✅ (필수)
├── requirements.txt         ✅ (필수)
├── Dockerfile               ✅ (필수)
├── templates/index.html     ✅ (필수)
└── knowledge_base/          ✅ (필수)
```

### 3.2 .env.local 파일 생성 (로컬 테스트용)

```bash
# AI스타트업 RAG 폴더에서
cp .env.example .env.local

# .env.local 편집
# OPENAI_API_KEY=sk-your-key
```

### 3.3 로컬에서 테스트 (선택사항)

```bash
# 1. 가상 환경
python -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 로드
export OPENAI_API_KEY=sk-your-key

# 4. 실행
python app.py

# 5. 테스트
# http://localhost:5000 방문
```

---

## 4️⃣ Google Cloud Run에 배포 (10분)

### 방법 A: 간단한 배포 (권장) 🟢

**한 줄 명령으로 배포:**

```bash
cd /path/to/AI스타트업\ RAG

gcloud run deploy ai-startup-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars \
    OPENAI_API_KEY=sk-your-key,\
    MODEL_NAME=gpt-3.5-turbo,\
    DEBUG=False
```

**설명:**
- `--source .` : 현재 폴더에서 배포
- `--platform managed` : 관리형 Cloud Run
- `--region us-central1` : 미국 중부 (가장 저렴)
- `--allow-unauthenticated` : 누구나 접속 가능
- `--set-env-vars` : 환경 변수 설정

### 배포 진행 과정

```
🔨 Building your service...

Logs are available at [URL]

Building and deploying...
✓ Building step finished
✓ Deploying to Cloud Run...
✓ Deployment succeeded!

Service deployed to: https://ai-startup-rag-xxxxx.run.app
```

**축하합니다! 배포 완료!** 🎉

---

## 5️⃣ 배포 확인 및 관리

### 5.1 배포된 서비스 확인

```bash
# 배포된 서비스 목록
gcloud run services list

# 출력:
# SERVICE                 REGION        URL
# ai-startup-rag          us-central1   https://ai-startup-rag-xxxxx.run.app
```

### 5.2 웹에서 접속

```
https://ai-startup-rag-xxxxx.run.app
```

브라우저에서 위 URL을 열면:
- ✅ 웹 인터페이스 표시
- ✅ 질문 입력 가능
- ✅ AI 답변 받기 가능

### 5.3 로그 확인

```bash
# 실시간 로그 보기
gcloud run logs read ai-startup-rag --limit 50 --region us-central1

# 특정 시간 로그
gcloud run logs read ai-startup-rag --limit 100
```

---

## 6️⃣ 환경 변수 업데이트

배포 후 환경 변수를 변경하려면:

```bash
# 방법 1: 명령어로 업데이트
gcloud run deploy ai-startup-rag \
  --update-env-vars OPENAI_API_KEY=sk-new-key \
  --region us-central1

# 방법 2: Cloud Console에서 편집
# 1. Cloud Console 방문
# 2. Cloud Run → ai-startup-rag 클릭
# 3. 환경 탭
# 4. 변수 수정 → 배포
```

---

## 7️⃣ 코드 업데이트

### 로컬 변경 후 재배포

```bash
# 1. 로컬에서 파일 수정

# 2. 다시 배포 (이전 서비스 업데이트)
gcloud run deploy ai-startup-rag \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**간단합니다!** 동일 이름으로 배포하면 자동으로 업데이트됩니다.

---

## 8️⃣ 지식 기반 (Knowledge Base) 업데이트

### 방법 1: 로컬에서 수정 후 재배포

```bash
# 1. 로컬 knowledge_base/ 폴더 수정
# 2. 파일 추가/수정

# 3. 다시 배포
gcloud run deploy ai-startup-rag \
  --source . \
  --region us-central1
```

### 방법 2: Google Cloud에서 직접 수정

배포 후 지식을 추가하려면:

```bash
# Cloud Storage에 파일 업로드
gsutil cp knowledge_base/raw/*.md gs://ai-startup-rag-data/raw/

# 서비스가 실행 중이면:
# 1. Cloud Run 재배포
# 2. 또는 API 엔드포인트 호출: /api/rebuild
```

---

## 📊 Google Cloud 비용

### 무료 범위 (매달)

| 항목 | 무료 한도 |
|------|---------|
| Cloud Run | 200만 요청 |
| 계산 시간 | 180,000 vCPU초 (~50시간) |
| 네트워크 | 1GB 인그레스/1GB 이그레스 |
| **월 비용** | **$0** (초과하지 않으면) |

### 예상 비용 (초과 시)

| 사용량 | 월 비용 |
|-------|--------|
| 10만 요청 | ~$0.40 |
| 100만 요청 | ~$4 |
| 1,000만 요청 | ~$40 |

**OpenAI API 비용이 훨씬 큽니다!**
- GPT-3.5-turbo: 입력 $0.5/M, 출력 $1.5/M

---

## 🔒 보안 설정

### 1. 환경 변수 보호

```bash
# .env.local은 절대 푸시하지 않기!
# 배포할 때만 사용

# 안전한 방법:
# 1. 로컬: export OPENAI_API_KEY=sk-...
# 2. 배포: --set-env-vars로 직접 설정
```

### 2. CORS 설정 (선택)

특정 도메인만 접속 허용:

**app.py 수정:**
```python
from flask_cors import CORS

allowed_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
```

**배포:**
```bash
gcloud run deploy ai-startup-rag \
  --set-env-vars CORS_ORIGINS=https://yourdomain.com \
  --region us-central1
```

### 3. 인증 추가 (선택)

원하는 사람만 접속하도록:

```bash
# --no-allow-unauthenticated 사용
gcloud run deploy ai-startup-rag \
  --source . \
  --no-allow-unauthenticated \
  --region us-central1

# 접속하려면 IAM 설정 필요
```

---

## 📈 모니터링

### Cloud Console에서 모니터링

1. **[Cloud Console](https://console.cloud.google.com)** 방문
2. **Cloud Run** → **ai-startup-rag** 클릭
3. **메트릭** 탭:
   - 요청 수
   - 응답 시간
   - 에러율
   - 메모리 사용량

### 경보 설정

```bash
# 에러율이 높으면 알림
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

---

## 🆘 문제 해결

### 문제: "Deployment failed"

```bash
# 1. 로그 확인
gcloud run logs read ai-startup-rag --limit 50

# 2. Dockerfile 확인
docker build -t ai-startup-rag .

# 3. requirements.txt 확인
pip install -r requirements.txt
```

### 문제: "API 키 오류"

```bash
# 환경 변수 확인
gcloud run services describe ai-startup-rag --region us-central1

# 다시 설정
gcloud run deploy ai-startup-rag \
  --set-env-vars OPENAI_API_KEY=sk-new-key \
  --region us-central1
```

### 문제: "Timeout"

응답이 30초 이상 걸리면:

```bash
# 1. 타임아웃 증가 (최대 3600초)
gcloud run deploy ai-startup-rag \
  --timeout 300 \
  --region us-central1

# 2. 문서 수 줄이기
# 3. 메모리 증가
gcloud run deploy ai-startup-rag \
  --memory 2Gi \
  --region us-central1
```

---

## 📱 자신의 도메인 연결

### Google Cloud 도메인 사용

```bash
# 1. Cloud Domains에서 도메인 구입
# 2. Cloud Run 서비스에 매핑

gcloud run services update-traffic ai-startup-rag \
  --to-revisions LATEST=100 \
  --region us-central1
```

### 다른 도메인 연결

```
1. DNS 레코드 설정:
   Type: CNAME
   Name: api
   Value: ai-startup-rag-xxxxx.run.app

2. Cloud Run > ai-startup-rag > 관리 도메인
3. 매핑 추가: api.yourdomain.com
```

---

## 🔄 자동 배포 (Cloud Build)

GitHub 없이 자동 배포:

### 1. Cloud Source Repositories 사용

```bash
# Google Cloud의 Git 저장소 생성
gcloud source repos create ai-startup-rag

# 로컬 저장소 연동
git config credential.helper gcloud.sh
git remote add origin \
  https://source.developers.google.com/p/ai-startup-rag/r/ai-startup-rag

# 푸시
git push -u origin main
```

### 2. Cloud Build 자동 배포

**cloudbuild.yaml 생성:**

```yaml
steps:
  # 1. Docker 이미지 빌드
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-startup-rag:latest', '.']

  # 2. 이미지 푸시
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ai-startup-rag:latest']

  # 3. Cloud Run에 배포
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --filename=.
      - --image=gcr.io/$PROJECT_ID/ai-startup-rag:latest
      - --location=us-central1
      - --output=out

images:
  - 'gcr.io/$PROJECT_ID/ai-startup-rag:latest'

options:
  machineType: 'N1_HIGHCPU_8'
```

**자동 배포 연동:**

```bash
gcloud builds submit --config=cloudbuild.yaml
```

---

## 📋 배포 체크리스트

- [ ] Google Cloud 계정 생성
- [ ] 프로젝트 생성 (ai-startup-rag)
- [ ] 필수 API 활성화
  - [ ] Cloud Run API
  - [ ] Artifact Registry API
  - [ ] Cloud Build API
- [ ] gcloud CLI 설치 및 로그인
- [ ] 프로젝트 설정 (`gcloud config set`)
- [ ] 로컬에서 테스트 (선택)
- [ ] Google Cloud에 배포
- [ ] URL에서 접속 확인
- [ ] 환경 변수 설정 확인
- [ ] 로그 확인
- [ ] 모니터링 설정

---

## 🎯 다음 단계

### 1. 지금 배포하기

```bash
gcloud run deploy ai-startup-rag \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-your-key
```

### 2. 도메인 설정

사용자 정의 도메인 연결 (선택)

### 3. 모니터링

Cloud Console에서 메트릭 확인

### 4. 지속적 배포

코드 변경 시 재배포

---

## 🔗 유용한 링크

- 📚 [Google Cloud Run 문서](https://cloud.google.com/run/docs)
- 🔧 [gcloud CLI 참고](https://cloud.google.com/sdk/gcloud)
- 💰 [가격 계산기](https://cloud.google.com/products/calculator)
- 📊 [Cloud Console](https://console.cloud.google.com)

---

## ✅ 완료!

이제 GitHub 없이 **Google Cloud만으로** 완전히 배포되었습니다!

**특징:**
- ✅ 웹에서 언제든 접속 가능
- ✅ 거의 무료 (월 $0-5)
- ✅ 자동 확장 (트래픽 증가 시)
- ✅ 간단한 코드 업데이트
- ✅ 내장 모니터링

**URL 공유:**
```
https://ai-startup-rag-xxxxx.run.app
```

---

**축하합니다! Google Cloud Run에서 당신의 RAG 챗봇이 실행 중입니다! 🚀**

*마지막 업데이트: 2024년 1월*
