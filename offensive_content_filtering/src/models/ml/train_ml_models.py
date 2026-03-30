# src/experiments/train_ml_models.py

import os
import joblib
import fasttext

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier

from offensive_content_filtering.src.models.ml.vectorizers import (
    TfidfVectorizerWrapper,
    FastTextVectorizer,
    CombinedVectorizer
)
from offensive_content_filtering.src.models.ml.preprocessing import preprocess_text


def train_and_save(texts, labels, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    # ========================
    # VECTORIZERS
    # ========================

    word_vec = TfidfVectorizerWrapper(
        TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=15000,
            token_pattern=r'(?u)\b\w+\b'
        ),
        preprocessor=preprocess_text
    )

    char_vec = TfidfVectorizerWrapper(
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=30000
        ),
        preprocessor=preprocess_text
    )

    ft_model = fasttext.load_model("embeddings.bin")

    scaler = StandardScaler()

    ft_vec = FastTextVectorizer(
        ft_model,
        scaler=scaler,
        preprocessor=preprocess_text
    )

    vectorizer_configs = {
        "word": CombinedVectorizer([word_vec]),
        "word_char": CombinedVectorizer([word_vec, char_vec]),
        "all": CombinedVectorizer([word_vec, char_vec, ft_vec]),
    }

    model_configs = {
        "svm": LinearSVC(C=1.0),
        "xgb": XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        )
    }

    # ========================
    # TRAIN LOOP
    # ========================

    for vec_name, vectorizer in vectorizer_configs.items():

        X = vectorizer.fit(texts).transform(texts)

        # ⚠️ IMPORTANT: fit scaler AFTER computing vectors
        if hasattr(ft_vec, "scaler") and ft_vec.scaler:
            ft_vec.scaler.fit(X.toarray())

        for model_name, model in model_configs.items():

            name = f"{vec_name}_{model_name}"
            print(f"🚀 Training {name}")

            model.fit(X, labels)

            # 🔥🔥🔥 THIS IS THE IMPORTANT PART 🔥🔥🔥
            joblib.dump(model, f"{output_dir}/{name}_model.pkl")
            joblib.dump(vectorizer, f"{output_dir}/{name}_vectorizer.pkl")