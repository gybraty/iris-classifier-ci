import pytest

from app.model import MODEL_VERSION, SPECIES, IrisClassifier


@pytest.fixture(scope="module")
def classifier() -> IrisClassifier:
    return IrisClassifier()


def test_accuracy_meets_baseline(classifier):
    assert classifier.info.test_accuracy >= 0.85


def test_prediction_of_clear_setosa(classifier):
    prediction = classifier.predict([5.1, 3.5, 1.4, 0.2])
    assert prediction.species == "setosa"
    assert prediction.confidence > 0.5


def test_prediction_of_clear_virginica(classifier):
    prediction = classifier.predict([6.5, 3.0, 5.8, 2.2])
    assert prediction.species == "virginica"


def test_probabilities_sum_to_one(classifier):
    prediction = classifier.predict([5.9, 3.0, 4.2, 1.5])
    assert set(prediction.probabilities) == set(SPECIES)
    assert sum(prediction.probabilities.values()) == pytest.approx(1.0, abs=1e-3)


def test_wrong_number_of_features_rejected(classifier):
    with pytest.raises(ValueError):
        classifier.predict([5.1, 3.5, 1.4])


def test_model_version_is_exposed():
    assert MODEL_VERSION
