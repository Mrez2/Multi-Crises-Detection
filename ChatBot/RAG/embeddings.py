from sklearn.feature_extraction.text import TfidfVectorizer

class EmbeddingEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.fitted = False

    def fit_transform(self, texts):
        """Fit vectorizer on dataset texts and generate document embeddings."""
        if not texts:
            return None
        matrix = self.vectorizer.fit_transform(texts)
        self.fitted = True
        return matrix

    def transform(self, query):
        """Vectorize a single query string using fitted vocabulary."""
        if not self.fitted:
            return None
        return self.vectorizer.transform([query])