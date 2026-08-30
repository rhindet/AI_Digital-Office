from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.services.knowledge_service import (
    ask_knowledge_base,
)

from app.services.knowledge_ingestion import (
    ingest_document,
)


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"],
)


KNOWLEDGE_DIR = Path("app/knowledge")

KNOWLEDGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/ask")
async def ask_knowledge(
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await ask_knowledge_base(
        db=db,
        question=question,
    )

    return result


@router.post("/upload")
async def upload_knowledge_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Solamente soporte y administradores
    # pueden agregar documentos.
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to upload knowledge documents",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    allowed_extensions = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported",
        )

    file_path = KNOWLEDGE_DIR / file.filename

    content = await file.read()

    file_path.write_bytes(content)

    try:

        chunks = ingest_document(
            db=db,
            file_path=str(file_path),
        )

    except Exception:

        if file_path.exists():
            file_path.unlink()

        raise

    return {
        "message": "Document uploaded successfully",
        "document": file.filename,
        "chunks_created": len(chunks),
    }