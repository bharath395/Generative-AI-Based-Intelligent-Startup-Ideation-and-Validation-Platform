import math
import os

_sentence_model = None

def generate_simple_embedding(text):
    """
    Generates a normalized 16-dimensional semantic vector representation for RAG retrieval.
    """
    text = (text or "").lower()
    vocab = ['ai', 'market', 'tech', 'student', 'app', 'saas', 'data', 'finance', 'agri', 'health', 'code', 'cloud', 'user', 'growth', 'web', 'mobile']
    vector = []
    
    for word in vocab:
        count = text.count(word)
        vector.append(float(count))

    norm = math.sqrt(sum(v*v for v in vector)) or 1.0
    return [v / norm for v in vector]


def generate_sentence_transformer_embedding(text):
    """
    Generates embeddings with Sentence Transformers when explicitly enabled.
    Falls back to the lightweight local embedding if the model is unavailable.
    """
    global _sentence_model
    if os.getenv("ENABLE_SENTENCE_TRANSFORMERS", "0") != "1":
        return generate_simple_embedding(text)

    try:
        from sentence_transformers import SentenceTransformer
        if _sentence_model is None:
            model_name = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
            _sentence_model = SentenceTransformer(model_name)
        vector = _sentence_model.encode(text or "", normalize_embeddings=True)
        return vector.tolist()
    except Exception:
        return generate_simple_embedding(text)

def cosine_similarity(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))
