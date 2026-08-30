from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.ai_copilot import AICopilotRequest

from app.services.ai_copilot import (
    chat_with_copilot,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI Copilot"],
)


@router.post("/chat")
async def ai_chat(
    data: AICopilotRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        result = await chat_with_copilot(
            db=db,
            user_id=current_user.id,
            conversation_id=data.conversation_id,
            message=data.message,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )