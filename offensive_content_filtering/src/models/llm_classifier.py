# src/models/llm_classifier.py
from offensive_content_filtering.src.models.base_classifier import BaseClassifier
from offensive_content_filtering.src.models.llm_providers.base_llm_provider import BaseLLMProvider

class LLMClassifier(BaseClassifier):
    """
    LLM classifier wrapper that delegates to a provider.
    """

    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    def predict(self, text: str):
        """
        Calls provider.predict and returns BaseClassifier format:
        offensive: bool
        score: float | None
        model_outputs: dict
        """
        return self.provider.predict(text)