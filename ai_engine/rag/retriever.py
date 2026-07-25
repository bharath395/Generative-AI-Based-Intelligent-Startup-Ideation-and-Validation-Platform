from ai_engine.rag.document_loader import load_knowledge_documents
from ai_engine.rag.embeddings import (
    cosine_similarity,
    generate_sentence_transformer_embedding,
)
from config import DATABASE_DIR

class KnowledgeRetriever:
    def __init__ (self):
        self.docs = load_knowledge_documents()
        self.collection = None
        for doc in self.docs:
            doc['embedding'] = generate_sentence_transformer_embedding(doc['content'])
        self._initialize_chroma_collection()

    def _initialize_chroma_collection(self):
        try:
            import chromadb
            chroma_dir = DATABASE_DIR / "chroma_store"
            chroma_dir.mkdir(parents=True, exist_ok=True)
            client = chromadb.PersistentClient(path=str(chroma_dir))
            self.collection = client.get_or_create_collection("startup_knowledge")
            ids = [f"doc-{index}" for index, _ in enumerate(self.docs)]
            self.collection.upsert(
                ids=ids,
                embeddings=[doc["embedding"] for doc in self.docs],
                documents=[doc["content"] for doc in self.docs],
                metadatas=[
                    {"title": doc["title"], "category": doc["category"]}
                    for doc in self.docs
                ],
            )
        except Exception:
            self.collection = None

    def query(self, query_text, top_k=2):
        query_vector = generate_sentence_transformer_embedding(query_text)
        if self.collection:
            try:
                result = self.collection.query(
                    query_embeddings=[query_vector],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"],
                )
                docs = []
                documents = result.get("documents", [[]])[0]
                metadatas = result.get("metadatas", [[]])[0]
                distances = result.get("distances", [[]])[0]
                for content, metadata, distance in zip(documents, metadatas, distances):
                    docs.append({
                        "category": metadata.get("category", "Knowledge"),
                        "title": metadata.get("title", "Knowledge Base Result"),
                        "content": content,
                        "score": round(1 / (1 + float(distance)), 4),
                    })
                if docs:
                    return docs
            except Exception:
                pass

        scored = []
        for doc in self.docs:
            sim = cosine_similarity(query_vector, doc['embedding'])
            scored.append((sim, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

retriever_instance = KnowledgeRetriever()
