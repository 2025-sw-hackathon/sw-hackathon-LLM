#!/usr/bin/env python
# core/vector_store.py
import os
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from config.settings import VECTOR_STORE_DIR, EMBEDDING_MODEL, DEVICE

def get_vector_store(docs: List[Document]):
    """문서 목록으로부터 벡터 스토어를 생성하거나 기존 인덱스를 로드합니다."""
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': DEVICE}
    )
    
    if os.path.exists(VECTOR_STORE_DIR) and os.listdir(VECTOR_STORE_DIR):
        vs = FAISS.load_local(
            VECTOR_STORE_DIR, embeddings,
            allow_dangerous_deserialization=True
        )
        print("🔁 기존 FAISS 인덱스 로드")
        return vs
    
    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(VECTOR_STORE_DIR)
    print("✨ 새로운 FAISS 인덱스 생성 및 저장")
    return vs