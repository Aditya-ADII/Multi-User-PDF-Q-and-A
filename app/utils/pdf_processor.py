import PyPDF2
import faiss
import numpy as np
from .embeddings import embed_text, embed_query
import os
import tempfile

def ingest_pdf(uploaded_file, user_id, redis_client):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(uploaded_file.read())
        pdf_path = temp_file.name

    try:
        with open(pdf_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        chunks = text.split('\n\n')
        embeddings = embed_text(chunks)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        redis_client.set_list(f"chunks:{user_id}", chunks)
        redis_client.set_embeddings(f"embeddings:{user_id}", embeddings)
        redis_client.set_embeddings(f"index:{user_id}", index)
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)

def retrieve_context(user_id, query, redis_client):
    embeddings = redis_client.get_embeddings(f"embeddings:{user_id}")
    index = redis_client.get_embeddings(f"index:{user_id}")
    chunks = redis_client.get_list(f"chunks:{user_id}")
    
    if embeddings is None or index is None or not chunks:
        return "No context available. Please upload a PDF."
    
    query_embedding = embed_query(query)
    query_embedding = np.array(query_embedding)
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)
    
    D, I = index.search(query_embedding, k=3)
    relevant_chunks = [chunks[i] for i in I[0] if i < len(chunks)]
    
    return " ".join(relevant_chunks)