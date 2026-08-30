import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.knowledge import KnowledgeChunk


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Usuario necesario para las pruebas de IA
    user = db.query(User).filter(User.id == 1).first()

    if not user:
        user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            password_hash="test_password",
            role="employee",
            is_active=True,
        )
        db.add(user)

    # Conocimiento necesario para las pruebas de búsqueda
    knowledge = db.query(KnowledgeChunk).first()

    if not knowledge:
        knowledge = KnowledgeChunk(
            document_name="VPN.pdf",
            content=(
                "Para conectarte a la VPN institucional "
                "debes utilizar el cliente VPN autorizado."
            ),
            embedding=[0.0] * 1536,
        )
        db.add(knowledge)

    db.commit()

    yield db

    db.close()