from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_nome_invalido():
    response = client.get("/api/v1/clima/X")
    assert response.status_code == 400
