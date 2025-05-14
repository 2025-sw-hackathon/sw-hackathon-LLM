#!/usr/bin/env python
# api/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Optional

# 모델 정의
class ChatHistoryItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    sessionId: str
    query: str
    chatHistory: Optional[List[ChatHistoryItem]] = []

class ChatResponse(BaseModel):
    answer: str
    sessionId: str
    sourceDocuments: Optional[List[str]] = []

# 추가: Spring API를 위한 간단한 요청 모델
class SimpleQuestion(BaseModel):
    question: str