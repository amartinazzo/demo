from demo.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is my model API."}

@pytest.mark.parametrize(
    "payload", [
        {"user_id": 1, "text": "eu gosto de"},
        {"text": "eu gosto de"}
        ])
def test_model_endpoint_with_correct_payload(payload):
    response = client.post("/model", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "generated_text" in data.keys()
    assert payload["text"] in data["generated_text"]

@pytest.mark.parametrize(
    "payload", [
        {"user_id": "texto", "text": "eu gosto de"},
        {"user_id": 1}
        ])
def test_model_endpoint_with_incorrect_payload(payload):
    response = client.post("/model", json=payload)
    assert response.status_code == 422
