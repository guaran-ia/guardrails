from abc import ABC, abstractmethod
from functools import lru_cache
import re

class BasePartitioner(ABC):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @abstractmethod
    def partition(self, text: str) -> list[str]:
        pass

class SentencePartitioner(BasePartitioner):

    def partition(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)

        max_tokens = self.tokenizer.max_tokens
        parts = []

        for sentence in sentences:
            if self.tokenizer.count_tokens(sentence) <= max_tokens:
                parts.append(sentence)
                continue

            tokens = self.tokenizer.tokenize(sentence)

            start = 0
            overlap = 0

            while start < len(tokens):
                sub_tokens = tokens[start:start + max_tokens]
                chunk_text = self.tokenizer.decode(sub_tokens)

                while self.tokenizer.count_tokens(chunk_text) > max_tokens:
                    sub_tokens = sub_tokens[:-1]
                    chunk_text = self.tokenizer.decode(sub_tokens)
                    overlap += 1

                parts.append(chunk_text)

                start += (max_tokens - overlap)
                overlap = 0

        return parts

class IterativePartitioner(BasePartitioner):

    def __init__(self, tokenizer):
        super().__init__(tokenizer)
        self.max_tokens = tokenizer.max_tokens

    @lru_cache(maxsize=10000)
    def _count_tokens(self, text: str) -> int:
        return self.tokenizer.count_tokens(text)

    def partition(self, text: str) -> list[str]:
        text = text.strip()

        if self._count_tokens(text) <= self.max_tokens:
            return [text]

        parts = []

        splitters = [
            r"\n\s*\n",            # paragraphs
            r"\n",                 # lines
            r"(?<=[.!?])\s+",      # sentences
            r"(?<=[,;:])\s+"       # clauses
        ]

        def recursive_split(segment: str, level: int):

            if self._count_tokens(segment) <= self.max_tokens:
                parts.append(segment.strip())
                return

            if level >= len(splitters):
                return

            pieces = re.split(splitters[level], segment)

            if level < len(splitters) - 1:
                for piece in pieces:
                    piece = piece.strip()
                    if piece:
                        recursive_split(piece, level + 1)
            else:
                current = ""

                for clause in pieces:
                    clause = clause.strip()
                    if not clause:
                        continue

                    candidate = (current + " " + clause).strip()

                    if self._count_tokens(candidate) <= self.max_tokens:
                        current = candidate
                    else:
                        if current:
                            parts.append(current.strip())

                        if self._count_tokens(clause) <= self.max_tokens:
                            current = clause
                        else:
                            current = ""

                if current:
                    parts.append(current.strip())

        recursive_split(text, 0)

        return parts