from pathlib import Path

from sqlalchemy.orm import Session
from pypdf import PdfReader
from docx import Document

from app.models.knowledge import KnowledgeChunk
from app.services.embedding_service import create_embedding


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def extract_text_from_pdf(
    file_path: str,
) -> str:

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_text_from_docx(
    file_path: str,
) -> str:

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


def extract_text(
    file_path: str,
) -> str:

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension in [".txt", ".md"]:

        return path.read_text(
            encoding="utf-8"
        )

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    if extension == ".docx":

        return extract_text_from_docx(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def ingest_document(
    db: Session,
    file_path: str,
):

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    # 1. Extraer texto
    text = extract_text(
        file_path
    )

    # 2. Dividir en chunks
    chunks = split_text(text)

    if not chunks:

        raise ValueError(
            "Document contains no readable text"
        )

    # 3. Eliminar versión anterior
    db.query(KnowledgeChunk).filter(
        KnowledgeChunk.document_name
        == path.name
    ).delete(
        synchronize_session=False
    )

    created_chunks = []

    # 4. Crear embeddings
    for chunk_text in chunks:

        embedding = create_embedding(
            chunk_text
        )

        chunk = KnowledgeChunk(
            document_name=path.name,
            content=chunk_text,
            embedding=embedding,
        )

        db.add(chunk)

        created_chunks.append(chunk)

    # 5. Guardar
    db.commit()

    return created_chunks