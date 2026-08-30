from app.database.database import SessionLocal

from app.services.knowledge_ingestion import (
    ingest_document,
)


db = SessionLocal()

try:

    chunks = ingest_document(
        db=db,
        file_path="app/knowledge/manual_wifi.txt",
    )

    print(
        f"Documento procesado correctamente."
    )

    print(
        f"Chunks creados: {len(chunks)}"
    )

    for chunk in chunks:

        print(
            f"ID: {chunk.id}"
        )

        print(
            f"Documento: {chunk.document_name}"
        )

        print(
            f"Contenido: {chunk.content}"
        )

        print("-" * 50)

finally:

    db.close()