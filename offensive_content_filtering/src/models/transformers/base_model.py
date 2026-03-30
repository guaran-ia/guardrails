from abc import ABC, abstractmethod

class BaseTransformerModel(ABC):
    """
    Base interface for transformer-based classification models.
    """

    def __init__(self, name: str, label_map: dict | None = None):
        self.name = name
        self.label_map = label_map or {}

    def normalize_label(self, label: str) -> str:
        return self.label_map.get(label, label)

    @abstractmethod
    def predict(self, text: str) -> tuple[str, float]:
        """
        Returns:
            label (str): e.g. "toxic"
            score (float): confidence
        """
        pass