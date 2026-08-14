"""S07 starter: categorical generative classification and smoothing."""
from __future__ import annotations
import numpy as np

def class_priors(feature_counts: np.ndarray) -> np.ndarray:
    """Return class proportions from a class-by-category count table."""
    return (feature_counts.sum(axis=1)/feature_counts.sum()).astype(np.float64)
    pass

def conditional_probabilities(feature_counts: np.ndarray, alpha: float) -> np.ndarray:
    """Return row-normalized class-conditional probabilities with additive alpha."""
    added = feature_counts + alpha
    return (added/added.sum(axis=1, keepdims=True)).astype(np.float64)
    pass

def log_joint_scores(priors: np.ndarray, conditionals: np.ndarray, category: int) -> np.ndarray:
    """Return log p(y) + log p(x=category | y) for each class."""
    return np.log(priors) + np.log(conditionals[:, category])
    pass

def predict_class(priors: np.ndarray, conditionals: np.ndarray, category: int) -> int:
    """Return the class index with the largest log-joint score."""
    scores = log_joint_scores(priors, conditionals, category)
    return int(scores.argmax())
    pass

def main() -> None:
    feature_counts = np.array([[3, 1, 0], [1, 4, 0]], dtype=np.int64)
    priors = class_priors(feature_counts)
    for alpha in (0.0, 1.0):
        probs = conditional_probabilities(feature_counts, alpha)
        scores = log_joint_scores(priors, probs, 2)
        print(alpha, probs, scores)
        if np.any(np.isfinite(scores)):
            print("prediction:", predict_class(priors, probs, 2))
        else:
            print("prediction: undefined (all scores are non-finite)")

if __name__ == "__main__": main()
