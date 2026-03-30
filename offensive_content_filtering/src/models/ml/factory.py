from .loaders import load_ml_model, load_vectorizer
from ..ml_classifier import MLClassifier


def build_ml_classifier(**kwargs):
    model_path = kwargs.get("model_path")
    vectorizer_path = kwargs.get("vectorizer_path")
    threshold = kwargs.get("threshold", 0.5)

    if not model_path or not vectorizer_path:
        raise ValueError("model_path and vectorizer_path are required")

    model = load_ml_model(model_path)
    vectorizer = load_vectorizer(vectorizer_path)

    return MLClassifier(model, vectorizer, threshold)