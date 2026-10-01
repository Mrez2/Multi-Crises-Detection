from sklearn.metrics.pairwise import cosine_similarity
from ChatBot.RAG.document_loader import DocumentLoader
from ChatBot.RAG.embeddings import EmbeddingEngine

class RAGRetriever:
    def __init__(self, kb_path="ChatBot/RAG/knowledge_base.json"):
        self.loader = DocumentLoader(kb_path)
        self.embedder = EmbeddingEngine()
        self.documents = []
        self.tfidf_matrix = None
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        """Initialize document loading and vector embedding generation."""
        self.documents = self.loader.load_documents()
        texts = [doc.get("content", "") for doc in self.documents if "content" in doc]
        if texts:
            self.tfidf_matrix = self.embedder.fit_transform(texts)

    def retrieve(self, user_query, top_k=2, min_similarity=0.1):
        """Query knowledge base and return top relevant context chunks."""
        if not self.documents or self.tfidf_matrix is None:
            return ""

        try:
            query_vector = self.embedder.transform(user_query)
            if query_vector is None:
                return ""

            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            top_indices = similarities.argsort()[-top_k:][::-1]

            retrieved_chunks = []
            for idx in top_indices:
                if similarities[idx] >= min_similarity:
                    retrieved_chunks.append(self.documents[idx]["content"])

            return "\n".join(retrieved_chunks)
        except Exception as e:
            print(f"[⚠️ RAGRetriever Error]: {e}")
            return ""

# Global instance ready for import in response_generator.py
retriever = RAGRetriever()