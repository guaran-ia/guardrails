from detoxify import Detoxify
from offensive_content_filtering.src.models.transformers.base_model import BaseTransformerModel

class DetoxifyModel(BaseTransformerModel):
    def __init__(self, model_name, threshold=0.05):
        super().__init__(model_name)

        self.pipeline = Detoxify(model_type='multilingual')
        self.threshold = threshold

    def predict(self, text: str):
        result = self.pipeline.predict(text)

        max_score = max(result.values())
        label = int(max_score > self.threshold)

        return label, float(max_score)