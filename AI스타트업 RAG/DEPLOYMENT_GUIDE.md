# 🚀 클라우드 배포 완전 가이드

AI Startup RAG Chatbot을 온라인으로 배포하여 다른 사람들이 웹에서 접속할 수 있도록 합니다.

---

## 📊 배포 옵션 비교

| 플랫폼 | 비용 | 난이도 | 장점 | 단점 |
|--------|------|--------|------|------|
| **Heroku** | 💰 무료~$14/월 | ⭐⭐ | 가장 쉬움, 자동 배포 | 무료 tier 제한 많음 |
| **Railway** | 💰 무료~$20/월 | ⭐⭐ | 쉬움, 넉넉한 무료 tier | 상대적으로 새로움 |
| **Google Cloud Run** | 💰 무료 (제한) | ⭐⭐⭐ | 저가, 확장성 좋음 | 설정이 조금 복잡 |
| **AWS** | 💰 $10~50/월 | ⭐⭐⭐⭐ | 매우 확장 가능 | 가장 복잡함 |
| **Azure** | 💰 $10~50/월 | ⭐⭐⭐ | 엔터프라이즈급 | 설정 복잡 |

**추천:** 처음 시작하면 **Heroku** (가장 쉬움) → 비용 절감 원하면 **Railway** 또는 **Google Cloud Run**

---

## 🔑 1단계: API 키 보안 설정

### 중앙 집중식 API 키 관리

모든 사용자가 같은 API 키를 사용하므로 서버에서만 관리합니다.

#### app.py 수정

서버에 인증 추가:

```python
# app.py 상단에 추가
from functools import wraps
from flask import request

API_KEY = os.getenv('APP_API_KEY', '')  # 선택적 앱 API 키

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # API 키 체크 (선택적)
        if API_KEY and request.headers.get('X-API-Key') != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# 채팅 엔드포인트에 적용 (선택적)
@app.route('/api/chat', methods=['POST'])
@require_api_key  # 이 줄 추가
def chat():
    # ... 기존 코드
```

#### 환경 변수 설정

배포 플랫폼에 다음 환경 변수를 설정합니다:

```env
# 필수
OPENAI_API_KEY=sk-...

# 선택적
APP_API_KEY=your-app-key-here
MODEL_NAME=gpt-3.5-turbo
DEBUG=False
PORT=5000

# 보안
CORS_ORIGINS=https://yourdomain.com
```

#### 보안 주의사항

⚠️ **절대 공개하지 말 것:**
- OpenAI API 키
- App API 키
- 데이터베이스 비밀번호

✅ **환경 변수에만 저장**
✅ **배포 플랫폼의 시크릿 관리자 사용**
✅ **Git에 커밋하지 않기**

---

## 💚 Option 1: Heroku (가장 쉬움)

**예상 비용:** 무료 또는 $14/월  
**배포 시간:** 10분  
**난이도:** ⭐⭐

### 1.1 사전 준비

```bash
# Heroku CLI 설치
# https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

# Heroku 로그인
heroku login
```

### 1.2 배포 파일 준비

**Procfile 생성:**
```bash
# 프로젝트 루트에 생성
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app" > Procfile
```

**runtime.txt 생성** (Python 버전 명시):
```bash
echo "python-3.10.13" > runtime.txt
```

### 1.3 Heroku 앱 생성 및 배포

```bash
# 1. Heroku 앱 생성
heroku create your-app-name
# 결과: https://your-app-name.herokuapp.com

# 2. 환경 변수 설정
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set MODEL_NAME=gpt-3.5-turbo
heroku config:set DEBUG=False

# 3. 빌드팩 설정
heroku buildpacks:set heroku/python

# 4. Git 배포 (또는 GitHub 연동)
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 1.4 배포 후 확인

```bash
# 로그 확인
heroku logs --tail

# 앱 열기
heroku open

# 앱 이름 확인
heroku apps
```

### 1.5 문제 해결

**문제:** "Cannot find module"
```bash
heroku logs --tail  # 에러 메시지 확인
heroku run pip list  # 설치된 패키지 확인
```

**문제:** "API 키 오류"
```bash
heroku config  # 환경 변수 확인
heroku config:set OPENAI_API_KEY=sk-...  # 다시 설정
```

### 1.6 Heroku 비용 절감

무료 tier 사용:
- 시간당 30분 이상 요청이 없으면 자동 슬립
- 한 달에 550 시간 제한
- 데이터베이스 없음 (메모리만 사용)

비용 발생 전에 업그레이드하면:
- Basic: $14/월 (24/7 실행)
- Standard: $50/월 (더 많은 리소스)

---

## 🚂 Option 2: Railway (권장)

**예상 비용:** 무료 또는 $5+/월  
**배포 시간:** 5분  
**난이도:** ⭐⭐

Railway는 Heroku의 좋은 대안입니다 - 더 넉넉한 무료 tier와 간단한 UI.

### 2.1 사전 준비

1. [Railway.app](https://railway.app) 방문
2. GitHub 계정으로 회원가입

### 2.2 배포

```bash
# 1. GitHub에 푸시 (필수)
git add .
git commit -m "Ready for Railway"
git push origin main

# 2. Railway 웹사이트에서:
# - "New Project" 클릭
# - "Deploy from GitHub" 선택
# - 저장소 선택
# - 자동 배포 시작
```

### 2.3 환경 변수 설정

Railway 대시보드에서:

1. Variables 탭 클릭
2. 각 변수 추가:
   - `OPENAI_API_KEY`: sk-...
   - `MODEL_NAME`: gpt-3.5-turbo
   - `DEBUG`: False
   - `PORT`: 5000

### 2.4 커스텀 도메인 (선택)

1. Networking 탭
2. "Custom Domain" 추가
3. DNS 레코드 설정

### 2.5 예상 결과

배포 후:
```
✅ https://ai-startup-rag-[random].railway.app
```

---

## ☁️ Option 3: Google Cloud Run (저가)

**예상 비용:** 거의 무료 (월 200만 건 요청까지 무료)  
**배포 시간:** 15분  
**난이도:** ⭐⭐⭐

### 3.1 Google Cloud 계정 설정

```bash
# 1. Google Cloud 콘솔 방문
# https://console.cloud.google.com

# 2. 새 프로젝트 생성
# Project > Create Project

# 3. 결제 활성화
# Billing > Link Billing Account

# 4. Cloud Run API 활성화
# APIs & Services > Enable APIs
# "Cloud Run API" 검색 및 활성화
```

### 3.2 로컬 배포 (gcloud CLI)

```bash
# 1. Google Cloud SDK 설치
# https://cloud.google.com/sdk/docs/install

# 2. 로그인
gcloud auth login

# 3. 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# 4. 이미지 빌드 및 배포
gcloud run deploy ai-startup-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-...,MODEL_NAME=gpt-3.5-turbo
```

### 3.3 배포 후 확인

```bash
# 배포된 URL 확인
gcloud run describe ai-startup-rag --region us-central1
```

### 3.4 환경 변수 업데이트

```bash
gcloud run deploy ai-startup-rag \
  --update-env-vars OPENAI_API_KEY=sk-new-key \
  --region us-central1
```

---

## 📦 Option 4: Docker Hub + 어디서든 실행

Docker 이미지를 Docker Hub에 업로드하여 누구나 쉽게 실행 가능하게 합니다.

### 4.1 Docker Hub 계정 생성

1. [Docker Hub](https://hub.docker.com) 방문
2. 회원가입 및 로그인

### 4.2 이미지 빌드 및 푸시

```bash
# 1. Docker 로그인
docker login

# 2. 이미지 빌드
docker build -t your-username/ai-startup-rag:latest .

# 3. Docker Hub에 푸시
docker push your-username/ai-startup-rag:latest

# 4. 태그 추가 (버전 관리)
docker tag your-username/ai-startup-rag:latest \
  your-username/ai-startup-rag:v1.0.0
docker push your-username/ai-startup-rag:v1.0.0
```

### 4.3 다른 사람이 사용하기

```bash
# 누구나 실행 가능
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-... \
  your-username/ai-startup-rag:latest

# 또는 Docker Compose로
docker-compose up
```

### 4.4 README에 사용법 추가

```markdown
## 🐳 Docker로 실행

### 사전 준비
- Docker 설치
- OpenAI API 키

### 실행 방법

```bash
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-your-key \
  -v $(pwd)/knowledge_base:/app/knowledge_base \
  your-username/ai-startup-rag:latest

# 또는 Docker Compose
docker-compose up
```

### 웹 접속
http://localhost:5000
```

---

## 📱 Option 5: AWS (확장성 최고)

**예상 비용:** $10~50/월  
**배포 시간:** 20분  
**난이도:** ⭐⭐⭐⭐

### 5.1 빠른 배포 (Elastic Beanstalk)

```bash
# 1. EB CLI 설치
pip install awsebcli

# 2. AWS 계정 설정
aws configure

# 3. Elastic Beanstalk 초기화
eb init -p python-3.10 ai-startup-rag --region us-east-1

# 4. 환경 생성 및 배포
eb create ai-startup-rag-env

# 5. 환경 변수 설정
eb setenv OPENAI_API_KEY=sk-... MODEL_NAME=gpt-3.5-turbo

# 6. 배포
eb deploy
```

### 5.2 URL 확인

```bash
eb open  # 브라우저에서 자동으로 열기
```

### 5.3 상태 모니터링

```bash
eb status
eb logs
```

---

## 🔐 보안 체크리스트

배포하기 전에 확인:

- [ ] `.env` 파일이 `.gitignore`에 있음
- [ ] OpenAI API 키가 환경 변수에만 있음
- [ ] 배포 플랫폼의 "Secrets" 또는 "Environment Variables"에 설정됨
- [ ] CORS 설정이 필요한 도메인만 포함
- [ ] HTTPS/SSL 활성화됨
- [ ] 디버그 모드 OFF (`DEBUG=False`)
- [ ] 로그에 민감한 정보 없음

---

## 📊 배포 후 모니터링

### 1. 로그 확인

**Heroku:**
```bash
heroku logs --tail
```

**Railway:**
Dashboard > Logs 탭

**Google Cloud Run:**
```bash
gcloud run logs read ai-startup-rag
```

### 2. 성능 모니터링

- 응답 시간 확인
- 에러율 모니터링
- API 사용량 추적

### 3. 비용 모니터링

각 플랫폼의 대시보드에서:
- 월간 비용 확인
- 리소스 사용량 추적
- 필요시 업그레이드

---

## 🔄 지속적 배포 (CD)

### GitHub Actions로 자동 배포

**.github/workflows/deploy.yml** 생성:

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```

---

## 📝 URL 및 접근

배포 후 사람들에게 공유할 수 있는 정보:

```markdown
## AI Startup RAG Chatbot 온라인

👉 **채팅하기:** https://your-domain.com

### 사용 방법
1. 위 링크 클릭
2. 질문 입력
3. AI의 답변 받기

### 예시 질문
- "What is an AI startup?"
- "Tell me about machine learning"
- "How do I build an AI product?"
```

---

## 🆘 문제 해결

### 문제: "Application error"

```bash
# 로그 확인
heroku logs --tail  # 또는 해당 플랫폼의 로그 확인

# 환경 변수 확인
heroku config
```

### 문제: "503 Service Unavailable"

서버가 응답하지 않음:
1. 로그 확인
2. 메모리 부족 여부 확인
3. API 키 유효성 확인

### 문제: "Timeout"

응답이 너무 오래 걸림:
1. 문서 수 줄이기
2. 청킹 크기 감소
3. 더 높은 tier로 업그레이드

---

## 💡 Best Practices

1. **버전 관리**
   ```bash
   git tag -a v1.0.0 -m "First production release"
   git push origin v1.0.0
   ```

2. **환경 분리**
   - 개발: 로컬
   - 스테이징: 테스트 배포
   - 프로덕션: 실제 사용

3. **백업**
   - 벡터 데이터베이스 정기적 백업
   - 환경 변수 기록

4. **업데이트**
   - 의존성 정기 업데이트
   - 보안 패치 적용

---

## 📞 지원

각 플랫폼별 지원:
- **Heroku:** https://devcenter.heroku.com
- **Railway:** https://docs.railway.app
- **Google Cloud:** https://cloud.google.com/docs
- **AWS:** https://aws.amazon.com/support
- **Docker:** https://docs.docker.com

---

**축하합니다! 이제 전 세계 누구나 당신의 RAG 챗봇에 접속할 수 있습니다! 🌍**

---

*마지막 업데이트: 2024년 1월*
