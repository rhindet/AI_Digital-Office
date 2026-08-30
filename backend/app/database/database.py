
###### Conectar FastAPI con PostgreSQL #####


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql://ai_admin:ai_password"
    "@localhost:5433/ai_digital_office"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,

)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)


# Necesitamos una sesión de PostgreSQL.

# Esta funcion será utilizada por FastAPI para abrir y cerrar conexiones correctamente.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


