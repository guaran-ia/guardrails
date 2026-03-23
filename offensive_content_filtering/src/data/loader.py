import os
import json
from offensive_content_filtering.src.data.document import Document
from offensive_content_filtering.src.data.hashing import make_doc_id
from urllib.parse import urlparse

def load_jsonl_documents(file_path: str):
    """Reads a JSONL file and yields Document objects."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"JSONL file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
                text = data.get("text", "")
                if not text:
                    continue

                source = None if data.get("source") in [None, "unknown"] else data.get("source")
                url = None if data.get("url") in [None, "unknown"] else data.get("url")
                domain = urlparse(url).netloc if url else None

                document = Document(
                    id=data.get("id") or make_doc_id(text),
                    text=text,
                    corpus=data.get("corpus"),
                    source=source,
                    url=url,
                    domain=domain,
                    num_words_split=data.get("num_words_split"),
                    num_words_punct_spacy=data.get("num_words_punct_spacy"),
                    num_words_no_punct_spacy=data.get("num_words_no_punct_spacy"),
                    num_chars=data.get("num_chars"),
                    metadata={k: v for k, v in data.items() if k not in ["text", "id", "corpus", 
                                                                        "source", "url", "num_words_split",
                                                                        "num_words_punct_spacy", 
                                                                        "num_words_no_punct_spacy",
                                                                        "num_chars"]}
                )
                yield document
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {line_number} in {file_path}") from e

def load_dataset(directory_path: str):
    """Reads all JSONL documents from a directory, yielding Document objects."""
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".jsonl"):
                for document in load_jsonl_documents(os.path.join(root, file)):
                    yield document