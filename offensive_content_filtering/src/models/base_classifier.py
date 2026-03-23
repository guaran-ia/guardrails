from abc import ABC, abstractmethod
from offensive_content_filtering.src.utils.prediction import Prediction
from offensive_content_filtering.src.data.document import Document

class BaseClassifier(ABC):

    @abstractmethod
    def predict(self, text: str) -> tuple[bool, float | None, dict]:
        """
        Returns:
            offensive: bool
            score: float or None
            model_outputs: dict
        """
        raise NotImplementedError


    def predict_document(self, document:Document):
        """
        Convenience method to work directly with Document objects.
        """

        offensive, score, model_outputs = self.predict(document.text)

        return Prediction(
            doc_id=document.id,
            corpus=document.corpus,
            offensive=offensive,
            score=score,
            model_outputs=model_outputs
        )