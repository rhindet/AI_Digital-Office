from app.services.knowledge_service import search_knowledge
def test_search_knowledge(db, monkeypatch):
    # Embedding controlado para la prueba.
    # Debe coincidir con el embedding del KnowledgeChunk
    # creado en conftest.py.
    test_embedding = [1.0] + [0.0] * 1535
    monkeypatch.setattr(
        "app.services.knowledge_service.create_embedding",
        lambda text: test_embedding,
    )
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
    # Como ambos embeddings son idénticos,
    # la distancia coseno debe ser aproximadamente 0.
    assert first_result["distance"] <= 0.45