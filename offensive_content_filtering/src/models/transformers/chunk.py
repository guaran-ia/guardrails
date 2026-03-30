from dataclasses import dataclass

@dataclass
class ChunkPrediction:
    label: str
    score: float
    chunk_id: int
    text: str
    tokens: int