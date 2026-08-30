from app.database.database import SessionLocal
from app.services.knowledge_service import search_knowledge


def test_search_knowledge():
    db = SessionLocal()

    try:
        results = search_knowledge(
            db=db,
            query="¿Cómo puedo conectarme a la VPN?",
        )

        assert results is not None
        assert isinstance(results, list)
        assert len(results) > 0

        first_result = results[0]

        assert "chunk" in first_result
        assert "distance" in first_result
        assert first_result["chunk"] is not None
        assert first_result["chunk"].id is not None
        assert first_result["chunk"].document_name
        assert first_result["chunk"].content

    finally:
        db.close()