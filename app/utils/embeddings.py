from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(texts):
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def embed_query(query):
    embedding = model.encode([query], convert_to_numpy=True)[0]
    return embedding