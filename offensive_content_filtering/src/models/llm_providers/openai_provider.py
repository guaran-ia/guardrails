# src/models/llm_providers/openai_grok.py
from offensive_content_filtering.src.models.llm_providers.base_llm_provider import BaseLLMProvider
from openai import OpenAI

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, endpoint: str, api_key: str, deployment: str):
        self.client = OpenAI(base_url=endpoint, api_key=api_key)
        self.deployment = deployment

    def predict(self, text: str):
        prompt = f"Clasifica el siguiente texto en guaraní o español como ofensivo o no ofensivo. Responde solo con 'Ofensivo' o 'No Ofensivo'.\n\nTexto: {text}"
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
        )
        llm_output = response.choices[0].message.content.strip()
        offensive = "1" in llm_output
        score = 1.0 if offensive else 0.0
        return offensive, score, {"raw_output": llm_output}