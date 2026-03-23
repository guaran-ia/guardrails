from abc import ABC, abstractmethod
from typing import Tuple, Dict

class BaseLLMProvider(ABC):
    @abstractmethod
    def predict(self, text: str) -> Tuple[bool, float | None, Dict]:
        """
        Predict whether a text is offensive.

        Returns:
            offensive: bool
            score: float or None
            model_outputs: dict (raw outputs, logs, etc.)
        """
        raise NotImplementedError