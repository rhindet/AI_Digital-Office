from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ai_chat_endpoint(client):

    response = client.post(
        "/ai/chat",
        json={
            "message": "¿Qué es inteligencia artificial?"
        },
    )

    assert response.status_code in [200, 401]