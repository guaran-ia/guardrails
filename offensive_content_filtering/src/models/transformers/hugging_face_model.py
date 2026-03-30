from offensive_content_filtering.src.models.transformers.base_model import BaseTransformerModel
from transformers import pipeline

class HuggingFaceModel(BaseTransformerModel):
    def __init__(self, model_path, model_name=None, label_map=None):
        model_name = model_name if model_name else model_path
        super().__init__(model_name, label_map)

        self.pipeline = pipeline(
            "text-classification",
            model=model_path,
            return_all_scores=False
        )

    def predict(self, text: str):
        result = self.pipeline(text)[0]
        label = self.normalize_label(result["label"])
        score = result["score"]
        return label, score