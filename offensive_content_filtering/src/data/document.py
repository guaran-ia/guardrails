from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Document:
    """Represents a single text document with optional metadata."""
    id: str
    text: str
    corpus: Optional[str] = None
    # optional stats for full corpus documents
    num_words_split: Optional[int] = None
    num_words_punct_spacy: Optional[int] = None
    num_words_no_punct_spacy: Optional[int] = None
    num_chars: Optional[int] = None
    source: Optional[str] = None
    url: Optional[str] = None
    domain: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
