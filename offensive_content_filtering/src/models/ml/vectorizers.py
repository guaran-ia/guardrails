import numpy as np
from scipy.sparse import hstack, csr_matrix


class TfidfVectorizerWrapper:
    def __init__(self, vectorizer, preprocessor=None):
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor

    def fit(self, texts):
        if self.preprocessor:
            texts = [self.preprocessor(t) for t in texts]
        self.vectorizer.fit(texts)
        return self

    def transform(self, texts):
        if self.preprocessor:
            texts = [self.preprocessor(t) for t in texts]
        return self.vectorizer.transform(texts)


class FastTextVectorizer:
    def __init__(self, model, scaler=None, preprocessor=None):
        self.model = model
        self.scaler = scaler
        self.preprocessor = preprocessor

    def _get_doc_vector(self, text):
        words = text.split()
        vectors = [self.model.get_word_vector(w) for w in words]

        if not vectors:
            return np.zeros(self.model.get_dimension())

        return np.mean(vectors, axis=0)

    def transform(self, texts):
        if self.preprocessor:
            texts = [self.preprocessor(t) for t in texts]

        vectors = np.array([self._get_doc_vector(t) for t in texts])

        if self.scaler:
            vectors = self.scaler.transform(vectors)

        return vectors


class CombinedVectorizer:
    """
    Combine multiple vectorizers (TF-IDF + FastText, etc.)
    """

    def __init__(self, vectorizers):
        self.vectorizers = vectorizers

    def fit(self, texts):
        for v in self.vectorizers:
            if hasattr(v, "fit"):
                v.fit(texts)
        return self

    def transform(self, texts):
        features = []

        for v in self.vectorizers:
            X = v.transform(texts)

            if isinstance(X, np.ndarray):
                X = csr_matrix(X)

            features.append(X)

        return hstack(features)