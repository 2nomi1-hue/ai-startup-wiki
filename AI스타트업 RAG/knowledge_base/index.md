# AI Startup RAG - 마스터 인덱스

이 파일은 전체 지식 기반의 구조와 내용을 정리한 마스터 인덱스입니다.

## 📚 지식 기반 구조

```
knowledge_base/
├── raw/              # RAW 강의 노트 및 수업 자료
├── wiki/             # Wiki 형식 문서 및 개념 설명
└── index.md          # 이 파일 (마스터 인덱스)
```

## 🎓 강의 노트 (raw/)

강의 노트는 시간순으로 정렬되어야 합니다.

### Week 1: AI Startup 기초
- `lecture_01_introduction.md` - AI 스타트업이란?
- `lecture_02_market_analysis.md` - 시장 분석 및 트렌드

### Week 2: 머신러닝 기초
- `lecture_03_ml_basics.md` - 머신러닝 개요
- `lecture_04_supervised_learning.md` - 지도 학습
- `lecture_05_unsupervised_learning.md` - 비지도 학습

### Week 3: AI 제품 개발
- `lecture_06_product_strategy.md` - AI 제품 전략
- `lecture_07_data_engineering.md` - 데이터 엔지니어링
- `lecture_08_model_deployment.md` - 모델 배포

## 📖 Wiki 문서 (wiki/)

Wiki 문서는 주제별로 정렬됩니다.

### 개념 정의
- `glossary.md` - 용어 정의
- `ml_concepts.md` - ML 개념 설명
- `business_concepts.md` - 비즈니스 개념

### 기술 가이드
- `tools_and_frameworks.md` - 도구 및 프레임워크
- `python_for_ml.md` - Python 머신러닝
- `data_processing.md` - 데이터 처리

### 사례 연구
- `case_studies.md` - 성공 사례 분석
- `lessons_learned.md` - 배운 교훈

## 🔍 주요 주제별 검색

### AI Startup 관련
- AI 스타트업의 정의
- 성공 요소
- 자금 조달
- 시장 기회

### 머신러닝
- 머신러닝 기초
- 알고리즘
- 모델 평가
- 하이퍼파라미터 튜닝

### 데이터
- 데이터 수집
- 데이터 정제
- 특성 엔지니어링
- 데이터 시각화

### 제품 개발
- MVP 전략
- 사용자 피드백
- 반복 개선
- 성과 지표

### 배포 및 운영
- 모델 배포
- A/B 테스트
- 모니터링
- 재학습 전략

## ✅ 문서 추가 체크리스트

새로운 문서를 추가할 때:

- [ ] 파일명을 명확하게 지음 (영문 권장)
- [ ] 마크다운 형식 사용 (.md)
- [ ] 문서 제목과 섹션 헤더 추가
- [ ] 목차(TOC) 포함 (긴 문서의 경우)
- [ ] 키워드와 개념 명확히 함
- [ ] 예시나 사례 포함
- [ ] 참고 자료 링크 추가
- [ ] index.md 업데이트
- [ ] 벡터 스토어 재구성: `curl -X POST http://localhost:5000/api/rebuild`

## 📝 마크다운 형식 예시

```markdown
# 제목 (Level 1)

## 소제목 (Level 2)

### 소소제목 (Level 3)

**굵은 텍스트**

*이탤릭 텍스트*

- 항목 1
- 항목 2
  - 하위 항목

1. 번호 항목 1
2. 번호 항목 2

> 인용문

\`\`\`python
# 코드 블록
print("Hello, World!")
\`\`\`

[링크 텍스트](https://example.com)
```

## 🚀 시작하기

1. **raw/ 폴더에 강의 노트 추가**
   ```bash
   cp lecture_notes/*.md knowledge_base/raw/
   ```

2. **wiki/ 폴더에 개념 문서 추가**
   ```bash
   cp wiki_docs/*.md knowledge_base/wiki/
   ```

3. **이 인덱스 파일 업데이트**
   - 새로운 문서 섹션 추가
   - 주요 주제 반영

4. **벡터 스토어 재구성**
   ```bash
   curl -X POST http://localhost:5000/api/rebuild
   ```

5. **채팅 시작**
   - http://localhost:5000 방문
   - 질문 입력

## 📊 최적화 팁

### 문서 구성
- 각 문서는 **2,000-5,000 단어** 정도가 최적
- 명확한 **섹션 헤더** 사용
- 복잡한 개념은 **예시와 함께 설명**

### 검색 최적화
- 파일명에 **키워드 포함**
- 문서 시작에 **요약 추가**
- **관련 개념 링크** 포함

### 품질 관리
- 정기적으로 **문서 검토**
- **오래된 정보 업데이트**
- **중복 제거** (여러 위치의 같은 내용)

---

**마지막 업데이트:** 2024년 1월

이 인덱스는 지식 기반 구조를 이해하고 새로운 문서를 추가하는 데 도움이 됩니다.
