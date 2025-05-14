#!/usr/bin/env python
# core/model.py
import torch
from typing import Tuple, List
from unsloth import FastLanguageModel
from config.settings import MODEL_ID, DEVICE

def load_llm() -> Tuple:
    """Unsloth LLM 모델과 토크나이저를 로드합니다."""
    print(f"🔄 Unsloth Gemma-3 ({MODEL_ID}) 모델 로드 중...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_ID,
        max_seq_length=4096,
        dtype=None,
        load_in_4bit=True,
    )
    return model, tokenizer

def prepare_prompt_template() -> str:
    """프롬프트 템플릿을 반환합니다."""
    system_tmpl = """
안녕하세요! 저는 Gemma-3 모델 기반의 대학 정보 안내 AI 도우미입니다 😊  
아래 <문서>를 참고하여 질문에 대해 한국어로 친절하고 따뜻하게,  
그리고 **최소 5문장 이상**으로 자세히 답변해드릴게요.  

<문서>
{context}

<질문>
{question}

<답변>
"""
    return system_tmpl

def generate_response(model, tokenizer, context: str, question: str, history_str: str = "") -> str:
    """모델을 사용하여 응답을 생성합니다."""
    # 시스템 프롬프트
    system_prompt = prepare_prompt_template().format(context=context, question=question)
    
    # 전체 프롬프트
    prompt = system_prompt + history_str
    
    # 토크나이즈 & 생성
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=False,
        temperature=1,
        top_p=1,
        top_k=1,
    )
    resp = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # prompt 부분 제거
    if "<|assistant|>" in resp:
        answer = resp.split("<|assistant|>")[-1].strip()
    elif "<답변>" in resp:
        answer = resp.split("<답변>")[-1].strip()
    else:
        answer = resp.strip()
    
    return answer

def get_source_documents(docs: List) -> List[str]:
    """검색된 문서로부터 소스 정보를 추출합니다."""
    source_documents = []
    for doc in docs:
        content = doc.page_content
        header_parts = content.split("\n")[0].split("|")
        if len(header_parts) > 0:
            source_documents.append(header_parts[0])
    
    # 중복 제거
    return list(set(source_documents))