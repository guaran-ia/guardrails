from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Prediction:
    doc_id:str
    corpus:str
    offensive:bool
    score:Optional[float]
    model_outputs: Optional[Dict[str, Any]] = None

