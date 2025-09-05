# 🎓 대학 정보 안내 챗봇 🤖

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemma](https://img.shields.io/badge/Gemma--3-FF6F00?style=for-the-badge&logo=google&logoColor=white)](https://blog.google/technology/ai/google-gemma-open-models/)

대학 정보 및 졸업 요건을 쉽게 안내해주는 AI 기반 챗봇 시스템입니다. Gemma-3 모델과 벡터 데이터베이스를 활용하여 학생들의 다양한 질문에 답변해드립니다! 🚀

## ✨ 주요 기능

- 🔍 **정확한 정보 검색**: 학과별 졸업 요건, 교과 과정, 학생 가이드 등을 빠르게 검색
- 💬 **자연스러운 대화**: 친절하고 따뜻한 어투로 학생들과 대화
- 🧠 **대화 맥락 기억**: 이전 대화를 기억하여 연속적인 질문에도 정확히 답변
- 🛠️ **Spring 연동 지원**: 기존 시스템과 쉽게 통합할 수 있는 API 제공

## 🏗️ 시스템 구조

```
university_chatbot/
│
├── app.py                 # 메인 애플리케이션 진입점
├── requirements.txt       # 필요한 패키지 목록
│
├── config/                # 설정 관련 모듈
│   ├── __init__.py
│   └── settings.py        # 환경 변수 및 설정
│
├── core/                  # 핵심 비즈니스 로직
│   ├── __init__.py
│   ├── data_loader.py     # JSON 데이터 로딩
│   ├── vector_store.py    # 벡터 스토어 관리
│   └── model.py           # LLM 모델 관리
│
└── api/                   # API 관련 모듈
    ├── __init__.py
    ├── schemas.py         # API 요청/응답 스키마
    └── routes.py          # API 엔드포인트
```

## 🚀 설치 및 실행 방법

### 준비물

- Python 3.8 이상
- CUDA 지원 GPU (권장) 🖥️
- 학과 졸업 요건 JSON 파일 (`json_to_text_entries.json`)

### 설치 단계

1. 저장소 클론하기

```bash
git clone https://github.com/your-username/university-chatbot.git
cd university-chatbot
```

2. 가상환경 생성 및 활성화 (선택사항)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정 (선택사항)

```bash
# Linux/Mac
export GRAD_JSON_PATH="path/to/json_to_text_entries.json"
export VECTOR_STORE_DIR="faiss_index"
export MODEL_ID="unsloth/gemma-3-1b-it-unsloth-bnb-4bit"

# Windows
set GRAD_JSON_PATH=path\to\json_to_text_entries.json
set VECTOR_STORE_DIR=faiss_index
set MODEL_ID=unsloth/gemma-3-1b-it-unsloth-bnb-4bit
```

### 다양한 실행 방법 👨‍💻

#### 1. 기본 실행 (터미널)

```bash
python app.py
```

브라우저에서 `http://localhost:8000/docs` 접속하여 API 문서 확인

#### 2. Docker 컨테이너로 실행 🐳

```bash
# Dockerfile 생성
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
EOF

# 이미지 빌드
docker build -t university-chatbot .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e GRAD_JSON_PATH=/app/json_to_text_entries.json \
  -v /path/to/your/json_to_text_entries.json:/app/json_to_text_entries.json \
  university-chatbot
```

#### 3. 개발 모드로 실행 (자동 리로드) 🔄

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. 프로덕션 모드로 실행 (Gunicorn)

```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 5. 백그라운드 실행 (nohup) 🔄

```bash
nohup python app.py > app.log 2>&1 &
echo $! > app.pid  # PID 저장
```

중지하려면:
```bash
kill $(cat app.pid)
```

## 🔄 API 엔드포인트

### 1. 채팅 API (`/api/chat`)

고급 채팅 기능을 위한 엔드포인트입니다.

**요청:**
```json
{
  "sessionId": "user123",
  "query": "컴퓨터공학과 졸업 요건이 뭐야?",
  "chatHistory": []
}
```

**응답:**
```json
{
  "answer": "컴퓨터공학과 졸업 요건에 대해 알려드릴게요...",
  "sessionId": "user123",
  "sourceDocuments": ["대학:서울대학교|학부:공과대학|전공:컴퓨터공학부"]
}
```

### 2. 간단한 채팅 API (`/api/simple-chat`)

Spring 애플리케이션과의 통합을 위한 간소화된 엔드포인트입니다.

**요청:**
```json
{
  "question": "컴퓨터공학과 졸업 요건이 뭐야?"
}
```

**응답:**
```json
{
  "llmResponse": "컴퓨터공학과 졸업 요건에 대해 알려드릴게요..."
}
```

## 📱 클라이언트 연동 예시

### cURL을 이용한 API 테스트 💻

```bash
curl -X 'POST' \
  'http://localhost:8000/api/simple-chat' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "컴퓨터공학과 졸업 요건이 뭐야?"
}'
```

### React를 이용한 웹 클라이언트 예시 ⚛️

```jsx
import { useState } from 'react';

function ChatComponent() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/simple-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      
      const data = await response.json();
      setAnswer(data.llmResponse);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-container">
      <h1>대학 정보 챗봇 🎓</h1>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="질문을 입력하세요..."
        />
        <button type="submit" disabled={loading}>
          {loading ? '처리 중...' : '질문하기'}
        </button>
      </form>
      
      {answer && (
        <div className="answer">
          <h3>답변:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
```

## 🧩 사용된 기술

- **FastAPI**: 고성능 웹 프레임워크
- **Unsloth**: 최적화된 Gemma-3 모델 실행
- **LangChain**: 언어 모델 애플리케이션 개발 프레임워크
- **FAISS**: 고효율 벡터 유사도 검색 라이브러리
- **HuggingFace Embeddings**: 한국어 특화 임베딩 모델

## 🌟 특징

- **한국어 특화**: 한국어로 자연스러운 대화가 가능한 모델 사용
- **빠른 응답**: 벡터 검색과 최적화된 모델로 빠른 응답 제공
- **확장 가능**: 모듈화된 구조로 새로운 기능 추가 용이
- **메모리 효율**: 4-bit 양자화로 메모리 사용량 최소화

## 📋 예시 질문

- "컴퓨터공학과 졸업 요건이 뭐야?" 🎓
- "공과대학 전공필수는 몇 학점이야?" 📚
- "수강신청은 어떻게 하는거야?" 📝
- "전과 신청 절차를 알려줘" 🔄
- "성적 평가 방식에 대해 알고 싶어" 📊

## 🔧 문제해결 팁

- **GPU 메모리 부족**: 더 작은 모델(gemma-2-2b)로 변경하거나 `MODEL_ID` 환경변수 조정
- **CUDA 오류**: CUDA 및 PyTorch 버전 호환성 확인 (CUDA 11.8 권장)
- **속도 개선**: 벡터 스토어 파라미터 튜닝 또는 더 빠른 임베딩 모델 사용
- **OOM 에러**: 최대 시퀀스 길이 줄이기 (`max_seq_length` 설정 조정)

## 🤝 기여하기

버그 리포트, 기능 요청, Pull Request 모두 환영합니다! 🙌

1. 저장소 포크하기
2. 기능 브랜치 생성하기 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋하기 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하기 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 🙏 감사의 말

- Google Gemma 팀의 훌륭한 오픈소스 모델 🌟
- Unsloth 팀의 최적화 도구 🦥

---

만든 이: 김석현 🧙‍♂️  
마지막 업데이트: 2025년 5월 15일 📅

---

⭐ 이 프로젝트가 마음에 드셨다면 Star를 눌러주세요! ⭐
