"""REST API that serves Iris species predictions."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.model import MODEL_VERSION, get_classifier

app = FastAPI(title="Iris Classifier API", version=MODEL_VERSION)


class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0, le=10, description="cm")
    sepal_width: float = Field(gt=0, le=10, description="cm")
    petal_length: float = Field(gt=0, le=10, description="cm")
    petal_width: float = Field(gt=0, le=10, description="cm")


class PredictionResponse(BaseModel):
    species: str
    confidence: float
    probabilities: dict[str, float]
    model_version: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model/info")
def model_info() -> dict:
    info = get_classifier().info
    return {
        "model_version": MODEL_VERSION,
        "test_accuracy": info.test_accuracy,
        "train_samples": info.train_samples,
        "test_samples": info.test_samples,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures) -> PredictionResponse:
    prediction = get_classifier().predict(
        [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width,
        ]
    )
    return PredictionResponse(
        species=prediction.species,
        confidence=prediction.confidence,
        probabilities=prediction.probabilities,
        model_version=MODEL_VERSION,
    )
