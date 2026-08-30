from app.database.database import SessionLocal
from app.services.ai_copilot import chat_with_copilot


class FakeResponse:
    output_text = "Respuesta simulada de OpenAI"


def test_chat_with_copilot(monkeypatch):

    def fake_create(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.ai_copilot.client.responses.create",
        fake_create,
    )

    db = SessionLocal()

    try:
        result = __import__(
            "asyncio"
        ).run(
            chat_with_copilot(
                db=db,
                user_id=1,
                conversation_id=None,
                message="¿Qué es inteligencia artificial?",
            )
        )

        assert result is not None
        assert "conversation_id" in result
        assert result["answer"] == "Respuesta simulada de OpenAI"
        assert result["question"] == "¿Qué es inteligencia artificial?"

    finally:
        db.close()