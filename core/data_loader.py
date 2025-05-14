#!/usr/bin/env python
# core/data_loader.py
import json
from typing import Dict, List
from langchain_core.documents import Document
from config.settings import GRAD_JSON_PATH, CHUNK_SIZE, OVERLAP

def load_grad_json(path: str = GRAD_JSON_PATH) -> Dict:
    """JSON 파일에서 학과 데이터를 로드합니다."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"🔄 JSON에서 {len(data.get('departments', []))}개 학과 데이터 로드 완료")
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {"departments": [], "student_guides": []}

def json_to_documents(json_data: Dict, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[Document]:
    """JSON 데이터를 Document 객체 리스트로 변환합니다."""
    docs = []
    
    # departments 배열을 순회
    if 'departments' in json_data:
        for department_data in json_data['departments']:
            college = department_data['college']
            faculty = department_data['faculty'] 
            dept = department_data['department']
            
            for block in department_data['graduation_requirements']:
                bid, title = block['id'], block['title']
                
                # 'periods' 키가 있는 경우와 없는 경우 처리
                if 'periods' in block:
                    for period, specs in block['periods'].items():
                        header = f"대학:{college}|학부:{faculty}|전공:{dept}|[{bid}] {title} - {period}\n"
                        lines = []
                        if isinstance(specs, dict):
                            for k, v in specs.items():
                                if v is None: continue
                                if isinstance(v, dict):
                                    sub = []
                                    for kk, vv in v.items():
                                        if isinstance(vv, list):
                                            vals = ','.join(f"{item['skill']}:{item['level']}" for item in vv)
                                            sub.append(f"{kk}:[{vals}]")
                                        else:
                                            sub.append(f"{kk}:{vv}")
                                    lines.append(f"- {k}: {'; '.join(sub)}")
                                else:
                                    lines.append(f"- {k}: {v}")
                        else:  # specs가 리스트인 경우
                            for item in specs:
                                lines.append(f"- {item['code']}: {item['description']}")
                        full = header + '\n'.join(lines)
                        words, step = full.split(), chunk_size - overlap
                        for i in range(0, len(words), step):
                            chunk = ' '.join(words[i:i+chunk_size])
                            docs.append(Document(page_content=chunk))
                elif 'options' in block:  # 컴퓨터학부 케이스 ('options' 키 존재)
                    header = f"대학:{college}|학부:{faculty}|전공:{dept}|[{bid}] {title}\n"
                    lines = []
                    for k, v in block['options'].items():
                        if v is None: continue
                        if isinstance(v, dict):
                            sub = []
                            for kk, vv in v.items():
                                sub.append(f"{kk}:{vv}")
                            lines.append(f"- {k}: {'; '.join(sub)}")
                        else:
                            lines.append(f"- {k}: {v}")
                    full = header + '\n'.join(lines)
                    words, step = full.split(), chunk_size - overlap
                    for i in range(0, len(words), step):
                        chunk = ' '.join(words[i:i+chunk_size])
                        docs.append(Document(page_content=chunk))
                elif 'description' in block:  # 컴퓨터학부 케이스 ('description' 키 존재)
                    header = f"대학:{college}|학부:{faculty}|전공:{dept}|[{bid}] {title}\n"
                    full = header + f"- {block['description']}"
                    words, step = full.split(), chunk_size - overlap
                    for i in range(0, len(words), step):
                        chunk = ' '.join(words[i:i+chunk_size])
                        docs.append(Document(page_content=chunk))
                elif 'requirements' in block:  # 'requirements' 키가 있는 경우 (정보통신학과 등)
                    header = f"대학:{college}|학부:{faculty}|전공:{dept}|[{bid}] {title}\n"
                    lines = []
                    for req in block['requirements']:
                        lines.append(f"- {req}")
                    full = header + '\n'.join(lines)
                    words, step = full.split(), chunk_size - overlap
                    for i in range(0, len(words), step):
                        chunk = ' '.join(words[i:i+chunk_size])
                        docs.append(Document(page_content=chunk))
    
    # student_guides 배열 처리
    if 'student_guides' in json_data:
        for guide in json_data['student_guides']:
            guide_id = guide['id']
            title = guide['title']
            
            header = f"학생가이드|[{guide_id}] {title}\n"
            content_parts = [f"설명: {guide['description']}"]
            
            # steps가 있는 경우 처리
            if 'steps' in guide:
                steps_text = "단계:\n" + '\n'.join([f"{i+1}. {step}" for i, step in enumerate(guide['steps'])])
                content_parts.append(steps_text)
            
            # links가 있는 경우 처리
            if 'links' in guide:
                links_text = "링크:\n" + '\n'.join([f"- {link['title']}: {link['url']}" for link in guide['links']])
                content_parts.append(links_text)
            
            # available_from이 있는 경우 처리
            if 'available_from' in guide:
                content_parts.append(f"사용 가능 시간: {guide['available_from']}")
            
            full = header + '\n'.join(content_parts)
            words, step = full.split(), chunk_size - overlap
            for i in range(0, len(words), step):
                chunk = ' '.join(words[i:i+chunk_size])
                docs.append(Document(page_content=chunk))
    
    print(f"✅ 총 {len(docs)}개의 Document 생성")
    return docs