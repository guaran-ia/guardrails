# src/models/llm_providers/vertex_ai.py
from offensive_content_filtering.src.models.llm_providers.base_llm_provider import BaseLLMProvider

class VertexAIProvider(BaseLLMProvider):
    def __init__(self, model_name: str):
        """
        Vertex AI provider. You will need to implement auth and chat API later.
        """
        self.model_name = model_name
        self.client = None  # placeholder for Vertex AI client

    def predict(self, text: str):
        # TODO: implement using VertexAI ChatModel
        llm_output = "0"  # temporary placeholder
        offensive = False
        score = 0.0
        return offensive, score, {"raw_output": llm_output}