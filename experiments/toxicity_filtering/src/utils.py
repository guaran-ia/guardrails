import json
from collections import Counter
import os

def read_jsonl(file_path: str):
    """Reads a JSONL (JSON Lines) file, yielding one JSON object per line."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"JSONL file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue  # skip empty lines

            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON on line {line_number} in {file_path}"
                ) from e

def write_jsonl(data:list, file_path:str, writing_mode='w'):
    try:
        with open(file_path, writing_mode, encoding='utf-8') as f:
            for item in data:
                json_string = json.dumps(item, ensure_ascii=False)
                f.write(json_string + '\n')
    except Exception as e:
        pass


def read_json(file_path: str):
    """Read a JSON file and return its contents as a Python object."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data, file_path: str, indent: int = 2):
    """Write a Python object to a JSON file."""
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def word_counts(text: str, words: list):
    """Counts the occurrences of each element of a list of words inside a given text."""
    text_lower = text.lower()
    counts = Counter()
    for entry in words:
        count = text_lower.count(entry.lower())
        if count:
            counts[entry.lower()] = count
    return dict(counts) if counts else []

def load_bad_words(file_path:str):
    """Load the bad words from a text file (one per line)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]