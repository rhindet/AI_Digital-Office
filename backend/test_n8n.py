import pytest

from app.services.n8n_service import send_to_n8n


class FakeResponse:

    status_code = 200
    content = b'{"response":"Respuesta simulada de n8n"}'
    headers = {
        "content-type": "application/json"
    }

    @property
    def text(self):
        return '{"response":"Respuesta simulada de n8n"}'

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "response": "Respuesta simulada de n8n"
        }


class FakeAsyncClient:

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def post(self, *args, **kwargs):
        return FakeResponse()


@pytest.mark.asyncio
async def test_send_to_n8n(monkeypatch):

    monkeypatch.setattr(
        "app.services.n8n_service.httpx.AsyncClient",
        lambda *args, **kwargs: FakeAsyncClient(),
    )

    result = await send_to_n8n(
        event="test",
        data={
            "message": "Hola desde pytest"
        },
    )

    assert result["response"] == "Respuesta simulada de n8n"