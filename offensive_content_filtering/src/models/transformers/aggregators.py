from .chunk import ChunkPrediction
from abc import ABC, abstractmethod
from collections import Counter, defaultdict

class BaseAggregator(ABC):
    @abstractmethod
    def aggregate(self, predictions: list[ChunkPrediction]) -> float:
        pass

class MajorityVoteAggregator(BaseAggregator):

    def aggregate(self, predictions):
        if not predictions:
            return 0.0

        labels = [p.label for p in predictions]
        counts = Counter(labels)

        _, votes = counts.most_common(1)[0]
        return votes / len(predictions)

class ScoreSumAggregator(BaseAggregator):

    def aggregate(self, predictions):
        if not predictions:
            return 0.0

        label_scores = defaultdict(float)

        for p in predictions:
            label_scores[p.label] += p.score

        return max(label_scores.values())
    
class WeightedAggregator(BaseAggregator):

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha

    def aggregate(self, predictions):
        if not predictions:
            return 0.0

        label_scores = defaultdict(float)

        for p in predictions:
            weight = p.score ** self.alpha
            label_scores[p.label] += weight

        return max(label_scores.values())