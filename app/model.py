"""Seeded Iris classifier shared by the API and the test suite.

The model is trained once at import time from the copy of the Iris dataset
bundled with scikit-learn, so no external data download is required and every
run starts from the same state (RANDOM_STATE is fixed).
"""

from dataclasses import dataclass
from functools import lru_cache

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
MODEL_VERSION = "1.0.0"
SPECIES = ("setosa", "versicolor", "virginica")


@dataclass(frozen=True)
class ModelInfo:
    test_accuracy: float
    train_samples: int
    test_samples: int


@dataclass(frozen=True)
class Prediction:
    species: str
    confidence: float
    probabilities: dict[str, float]


class IrisClassifier:
    """Random forest trained on the Iris dataset with a deterministic split."""

    def __init__(self, test_size: float = 0.2) -> None:
        iris = load_iris()
        x_train, x_test, y_train, y_test = train_test_split(
            iris.data,
            iris.target,
            test_size=test_size,
            random_state=RANDOM_STATE,
            stratify=iris.target,
        )
        self._model = RandomForestClassifier(
            n_estimators=100, random_state=RANDOM_STATE
        ).fit(x_train, y_train)
        self._info = ModelInfo(
            test_accuracy=float(self._model.score(x_test, y_test)),
            train_samples=len(x_train),
            test_samples=len(x_test),
        )

    @property
    def info(self) -> ModelInfo:
        return self._info

    def predict(self, features: list[float]) -> Prediction:
        if len(features) != 4:
            raise ValueError("expected exactly 4 feature values")
        proba = self._model.predict_proba([features])[0]
        index = int(proba.argmax())
        return Prediction(
            species=SPECIES[index],
            confidence=float(proba[index]),
            probabilities={
                SPECIES[i]: round(float(p), 4) for i, p in enumerate(proba)
            },
        )


@lru_cache(maxsize=1)
def get_classifier() -> IrisClassifier:
    """Build the classifier once per process."""
    return IrisClassifier()
