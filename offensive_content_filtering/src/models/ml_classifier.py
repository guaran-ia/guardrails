from offensive_content_filtering.src.models.base_classifier import BaseClassifier

class MLClassifier(BaseClassifier):

    def __init__(self, model, vectorizer, threshold: float = 0.5):
        self.model = model
        self.vectorizer = vectorizer
        self.threshold = threshold

    def predict(self, text: str):
        X = self.vectorizer.transform([text])

        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(X)[0][1]
        else:
            prob = float(self.model.predict(X)[0])

        offensive = prob >= self.threshold

        return offensive, float(prob), {
            "model_type": type(self.model).__name__
        }