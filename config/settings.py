# config/settings.py
import os
import torch

# 환경 변수 및 기본 설정
GRAD_JSON_PATH   = os.environ.get("GRAD_JSON_PATH", "json_to_text_entries.json")
VECTOR_STORE_DIR = os.environ.get("VECTOR_STORE_DIR", "faiss_index")
CHUNK_SIZE       = int(os.environ.get("CHUNK_SIZE", "800"))
OVERLAP          = int(os.environ.get("OVERLAP", "100"))
EMBEDDING_MODEL  = os.environ.get("EMBEDDING_MODEL", "snunlp/KR-SBERT-V40K-klueNLI-augSTS")
MODEL_ID         = os.environ.get("MODEL_ID", "unsloth/gemma-3-1b-it-unsloth-bnb-4bit")
DEVICE           = "cuda" if torch.cuda.is_available() else "cpu"
PORT             = int(os.environ.get("PORT", 8000))

# 세션별 대화 히스토리 저장 (메모리에 저장, 서버 재시작 시 초기화)
chat_histories = {}