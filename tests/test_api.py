from fastapi.testclient import TestClient
import pytest
import time
from statistics import mean

from demo.main import app

client = TestClient(app)

def test_root_endpoint_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is my model API."}

@pytest.mark.parametrize(
    "payload", [
        {"user_id": 1, "text": "eu gosto de"},
        {"text": "eu gosto de"}
        ])
def test_model_endpoint_receives_correct_payload(payload):
    response = client.post("/model", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert "generated_text" in data.keys()
    assert payload["text"] in data["generated_text"]

@pytest.mark.parametrize(
    "payload", [
        {"user_id": "texto", "text": "eu gosto de"},
        {"user_id": 1}
        ])
def test_model_endpoint_receives_incorrect_payload(payload):
    response = client.post("/model", json=payload)
    assert response.status_code == 422

@pytest.mark.parametrize(
    "payload", [
        {"text": "eu gosto de"}
        ])
def test_model_endpoint_returns_under_3s(payload):
    time_elapsed = []
    for _ in range(10):
        t0 = time.perf_counter()
        _ = client.post("/model", json=payload)
        time_elapsed.append(time.perf_counter() - t0)
    assert mean(time_elapsed) < 3