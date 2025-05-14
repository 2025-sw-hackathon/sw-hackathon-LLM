#!/usr/bin/env python
# api/routes.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from config.settings import chat_histories
from api.schemas import ChatRequest, ChatResponse, SimpleQuestion
from core.model import generate_response, get_source_documents

# FastAPI 애플리케이션 생성
app = FastAPI(title="대학 정보 안내 챗봇 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 변수
vector_store = None
model = None
tokenizer = None

def initialize_globals(vs, mdl, tkn):
    """글로벌 변수 초기화"""
    global vector_store, model, tokenizer
    vector_store = vs
    model = mdl
    tokenizer = tkn

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "LLM 서버가 정상 작동 중입니다."}

# 기존 채팅 엔드포인트
@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    global vector_store, model, tokenizer
    
    # 세션 ID 확인
    session_id = request.sessionId
    
    # 히스토리 가져오기 또는 생성
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    
    # 사용자의 입력에서 사용자 질의 추출
    query = request.query
    
    # 벡터 검색
    docs = vector_store.as_retriever(search_kwargs={"k": 3}).get_relevant_documents(query)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 히스토리 → 프롬프트 앞에 추가
    history_str = ""
    for item in chat_histories[session_id]:
        history_str += f"<|user|>\n{item['question']}\n</s>\n<|assistant|>\n{item['answer']}\n</s>\n"
    
    # 이번 질의 추가
    history_str += f"<|user|>\n{query}\n</s>\n<|assistant|>\n"
    
    # 응답 생성
    answer = generate_response(model, tokenizer, context, query, history_str)
    
    # 히스토리에 저장
    chat_histories[session_id].append({"question": query, "answer": answer})
    
    # 검색된 문서의 소스 추출
    source_documents = get_source_documents(docs)
    
    return ChatResponse(
        answer=answer,
        sessionId=session_id,
        sourceDocuments=source_documents
    )

# 추가: Spring API를 위한 간단한 채팅 엔드포인트
@app.post("/api/simple-chat")
async def simple_chat(request: SimpleQuestion) -> Dict[str, str]:
    global vector_store, model, tokenizer
    
    # 자동 세션 ID 생성
    session_id = f"spring-{len(chat_histories) + 1}"
    
    # 벡터 검색
    docs = vector_store.as_retriever(search_kwargs={"k": 3}).get_relevant_documents(request.question)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 이번 질의 추가
    history_str = f"<|user|>\n{request.question}\n</s>\n<|assistant|>\n"
    
    # 응답 생성
    answer = generate_response(model, tokenizer, context, request.question, history_str)
    
    # 간단한 응답만 반환 (Spring에서 기대하는 형식)
    return {"llmResponse": answer}