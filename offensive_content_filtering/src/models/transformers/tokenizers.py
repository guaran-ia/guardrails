from abc import ABC, abstractmethod

class BaseTokenizer(ABC):
    """
    Handles tokenization logic for transformer models.
    """

    @abstractmethod
    def tokenize(self, text: str) -> list[int]:
        pass

    @abstractmethod
    def decode(self, token_ids: list[int]) -> str:
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass

    @property
    @abstractmethod
    def max_tokens(self) -> int | None:
        pass


class HuggingFaceTokenizer(BaseTokenizer):
    def __init__(self, tokenizer, model_config):
        self.tokenizer = tokenizer
        self._max_tokens = (
            model_config.max_position_embeddings
            - tokenizer.num_special_tokens_to_add(pair=False)
        )

    def tokenize(self, text: str) -> list[int]:
        return self.tokenizer(text, add_special_tokens=True)["input_ids"]

    def decode(self, token_ids: list[int]) -> str:
        return self.tokenizer.decode(token_ids, skip_special_tokens=False)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenize(text))

    @property
    def max_tokens(self):
        return self._max_tokens

class DetoxifyTokenizer(HuggingFaceTokenizer):
    """
    Detoxify uses a HuggingFace tokenizer internally, so the logic gets reused.
    """
    pass