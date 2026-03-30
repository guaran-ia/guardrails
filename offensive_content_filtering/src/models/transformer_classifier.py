from typing import List
from offensive_content_filtering.src.models.base_classifier import BaseClassifier
from offensive_content_filtering.src.models.transformers.chunk import ChunkPrediction


class TransformerClassifier(BaseClassifier):
    """
    Classifier for transformer-based models with input size constraints.

    Pipeline:
        text → partition → model prediction per chunk → aggregation → final score
    """

    def __init__(
        self,
        model,
        tokenizer,
        partitioner,
        aggregator,
        threshold: float = 0.5
    ):
        """
        Args:
            model: BaseTransformerModel
            tokenizer: BaseTokenizer
            partitioner: BasePartitioner
            aggregator: BaseAggregator
            threshold (float): threshold for offensive classification
        """
        self.model = model
        self.tokenizer = tokenizer
        self.partitioner = partitioner
        self.aggregator = aggregator
        self.threshold = threshold

    def predict(self, text: str):
        """
        Predict offensiveness for a given text.

        Returns:
            offensive (bool)
            score (float)
            model_outputs (dict)
        """

        # 1️⃣ Partition text
        chunks = self.partitioner.partition(text)

        chunk_predictions: List[ChunkPrediction] = []

        # 2️⃣ Run model on each chunk
        for i, chunk in enumerate(chunks):
            label, score = self.model.predict(chunk)

            chunk_predictions.append(
                ChunkPrediction(
                    chunk_id=i,
                    text=chunk,
                    tokens=self.tokenizer.count_tokens(chunk),
                    label=label,
                    score=score
                )
            )

        # 3️⃣ Aggregate scores
        final_score = self.aggregator.aggregate(chunk_predictions)

        # 4️⃣ Final decision
        offensive = final_score >= self.threshold

        # 5️⃣ Build outputs
        model_outputs = {
            "model_name": self.model.name,
            "num_chunks": len(chunk_predictions),
            "chunks": [
                {
                    "chunk_id": c.chunk_id,
                    "score": c.score,
                    "label": c.label,
                    "tokens": c.tokens
                }
                for c in chunk_predictions
            ]
        }

        return offensive, final_score, model_outputs