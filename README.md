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
- 학과 졸업 요건 원대학교 학과별 정보 제공

---

만든 이: SeokHyun Kim 🧙‍♂️  
마지막 업데이트: 2025년 5월 15일 📅

---

⭐ 이 프로젝트가 마음에 드셨다면 Star를 눌러주세요! ⭐
