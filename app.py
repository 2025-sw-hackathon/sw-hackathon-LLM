#!/usr/bin/env python
# app.py
import uvicorn
from config.settings import PORT
from core.data_loader import load_grad_json, json_to_documents
from core.vector_store import get_vector_store
from core.model import load_llm
from api.routes import app, initialize_globals

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 초기화"""
    print("🚀 LLM 서버 초기화 중...")
    
    # JSON 데이터 로드
    json_data = load_grad_json()
    
    # 문서 생성
    documents = json_to_documents(json_data)
    
    # 벡터 스토어 생성/로드
    vector_store = get_vector_store(documents)
    
    # LLM 로드
    model, tokenizer = load_llm()
    
    # 전역 변수 초기화
    initialize_globals(vector_store, model, tokenizer)
    
    print("✅ 서버 초기화 완료!")

# 메인 실행 부분
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=False)