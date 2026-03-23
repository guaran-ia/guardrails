# src/models/llm_providers/azure_openai.py
from offensive_content_filtering.src.models.llm_providers.base_llm_provider import BaseLLMProvider
from openai import AzureOpenAI

class AzureOpenAIProvider(BaseLLMProvider):
    def __init__(self, endpoint: str, api_key: str, deployment: str, api_version: str, temperature = 0.1):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment = deployment
        self.temperature = temperature

    def predict(self, text: str):
        prompt = f"Clasifica el siguiente texto en guaraní o español como ofensivo o no ofensivo. Responde solo con 'Ofensivo' o 'No Ofensivo'.\n\nTexto: {text}"
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "Eres un linguista experto en guaraní y jopará. Tu trabajo es ayudar a resolver dudas sobre guarani."},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature
        )
        llm_output = response.choices[0].message.content.strip()
        offensive = "ofensivo" in llm_output.lower()
        score = 1.0 if offensive else 0.0
        return offensive, score, {"raw_output": llm_output}