# src/models/llm_providers/vertex_ai.py
from offensive_content_filtering.src.models.llm_providers.base_llm_provider import BaseLLMProvider
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional

class OffensiveResult(BaseModel):
    offensive:bool = Field(description="The veredict regarding whether the text is offensive or not.")
    reasoning:Optional[str] = Field(description="A concise explanation of why the text is offensive or not offensive.")

class VertexAIProvider(BaseLLMProvider):
    def __init__(self, model_name: str, api_key: str):
        """
        Vertex AI provider. A Gemini Model which decides whether a given
        """
        self.model = model_name
        self.client = genai.Client(api_key=api_key)

    def predict(self, text: str):
        system_instruction = "You are an expert linguist, specialised in Guarani, the language of the native people of Paraguay. You are aware of the nuances of the Guarani language and can distinguish the meaning of words based on context."

        prompt = f"Please classify the following text as offensive or not: \n\n {text}"

        response = self.client.models.generate_content(
            model = self.model,
            contents = prompt,
            config = types.GenerateContentConfig(
                system_instruction = system_instruction,
                response_mime_type = "application/json",
                response_json_schema = OffensiveResult.model_json_schema()
            )
        )

        offensive_result = OffensiveResult.model_validate_json(response.text)

        offensive = offensive_result.offensive
        score = 1 if offensive else 0

        return offensive, score, {"reasoning": offensive_result.reasoning}