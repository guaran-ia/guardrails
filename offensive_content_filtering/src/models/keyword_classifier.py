import re
import unicodedata
import csv

from collections import Counter

from offensive_content_filtering.src.models.base_classifier import BaseClassifier


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent matching.

    Steps:
        1. Convert to lowercase.
        2. Remove accents (keeping ñ).
        3. Reduce repeated letters (3+ → 2).

    Args:
        text (str): The raw text to normalize.

    Returns:
        str: Normalized text suitable for pattern matching.
    """

    text = text.lower()

    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    return text


def build_pattern(term: str) -> re.Pattern:
    """
    Build a regex pattern for a given term that is robust to repeated letters and phrases.

    Example:
        "stupid" → regex matches "stuupid", "stuuupid", etc.

    Args:
        term (str): Term or phrase to build pattern for.

    Returns:
        re.Pattern: Compiled regex pattern with word boundaries.
    """

    normalized = normalize_text(term)

    flexible_chars = []

    for char in normalized:
        if char.isalpha():
            #Match one or more consecutive ocurrences of each letter
            flexible_chars.append(f"{re.escape(char)}+")
        else:
            flexible_chars.append(re.escape(char))

    flexible_pattern = "".join(flexible_chars)

    return re.compile(rf"\b{flexible_pattern}\b")


def compile_terms(csv_path):
    """
    Compile offensive terms from CSV into regex patterns.

    CSV should have columns:
        - "term": offensive word or phrase
        - "severity": term severity score (float)

    Args:
        csv_path (str): Path to CSV file containing terms.

    Returns:
        List[Tuple[str, float, re.Pattern]]: List of (term, score, compiled_pattern)
    """

    compiled_terms = []

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            term = row["term"]
            severity = float(row["severity"])

            pattern = build_pattern(term)

            compiled_terms.append((term, severity, pattern))

    return compiled_terms


def count_score_toxic_terms(text: str, compiled_terms):
    """
    Count occurrences of toxic terms in text and compute a total offensiveness score.

    Args:
        text (str): Document text to evaluate.
        compiled_terms (List[Tuple[str, float, re.Pattern]]):
            List of compiled patterns with associated scores.

    Returns:
        Tuple[Dict[str, int], float]:
            - Dictionary of term → number of matches
            - Total document score (sum of term counts × score)
    """

    normalized_text = normalize_text(text)

    counts = Counter()
    document_score = 0

    for original_term, score, pattern in compiled_terms:

        matches = pattern.findall(normalized_text)

        if matches:
            counts[original_term] = len(matches)
            document_score += len(matches) * score

    return dict(counts), document_score



class KeywordClassifier(BaseClassifier):
    """
    Classifier that labels documents as offensive or not based on
    a list of pre-defined offensive terms and their scores.

    Attributes:
        compiled_terms (List[Tuple[str, float, re.Pattern]]):
            Compiled patterns with associated scores for fast matching.
    """

    def __init__(self, csv_path):
        """
        Initialize the classifier and compile terms.

        Args:
            csv_path (str): Path to CSV file containing offensive terms.
        """

        # compile everything once
        self.compiled_terms = compile_terms(csv_path)


    def predict(self, text):
        """
        Predict the offensiveness of a document.

        Args:
            text (str): Document text.

        Returns:
            Tuple[bool, float, dict]:
                - offensive: True or False
                - total_score: total offensiveness score
                - extras: dictionary containing term_counts
        """

        counts, total_score = count_score_toxic_terms(
            text,
            self.compiled_terms
        )

        offensive =  total_score > 0

        extras = {
            "term_counts": counts,
        }

        return offensive, total_score, extras