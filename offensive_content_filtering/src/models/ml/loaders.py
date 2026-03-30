import joblib


def load_ml_model(path: str):
    return joblib.load(path)


def load_vectorizer(path: str):
    return joblib.load(path)