import json
import os
from offensive_content_filtering.src.utils.prediction import Prediction

class PredictionWriter:
    """
    Writes Prediction objects to a JSONL file, handling optional fields
    and streaming large datasets safely.
    """

    def __init__(self, output_path: str, mode: str = "a"):
        """
        Initialize a PredictionWriter.

        Args:
            output_path (str): Path to output JSONL file.
            mode (str): File mode, "a" for append (default), "w" for overwrite.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.output_path = output_path
        self.mode = mode
        self.file = None

    def write(self, prediction: Prediction):
        """
        Write a single Prediction object to the output file.

        Handles optional fields like `score` and `model_outputs`.
        """
        if self.file is None:
            raise ValueError("File is not open. Use the context manager or open manually.")

        record = {
            "doc_id": getattr(prediction, "doc_id", None),
            "corpus": getattr(prediction, "corpus", None),
            "offensive": getattr(prediction, "offensive", None),
            "score": getattr(prediction, "score", None),
            "model_outputs": getattr(prediction, "model_outputs", {}) or {}
        }

        self.file.write(json.dumps(record) + "\n")

    # Optional: context manager support
    def __enter__(self):
        self.file = open(self.output_path, self.mode, encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
            self.file = None