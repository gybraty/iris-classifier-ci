from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_reports_accuracy():
    response = client.get("/model/info")
    assert response.status_code == 200
    assert response.json()["test_accuracy"] >= 0.9


def test_predict_returns_species():
    response = client.post("/predict", json=SAMPLE)
    assert response.status_code == 200
    body = response.json()
    assert body["species"] == "setosa"
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["model_version"]


def test_predict_rejects_missing_field():
    payload = dict(SAMPLE)
    del payload["petal_width"]
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_out_of_range_value():
    response = client.post("/predict", json={**SAMPLE, "sepal_length": 99})
    assert response.status_code == 422
