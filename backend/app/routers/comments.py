from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
)

from app.core.dependencies import get_current_user

from app.services.ticket_history import add_ticket_history
from app.services.notifications import create_notification


router = APIRouter(
    prefix="/tickets",
    tags=["Comments"],
)


@router.post(
    "/{ticket_id}/comments",
    response_model=CommentResponse,
)
def create_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if (
        current_user.role == "employee"
        and ticket.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to comment on this ticket",
        )

    comment = Comment(
        content=comment_data.content,
        ticket_id=ticket.id,
        user_id=current_user.id,
    )

    db.add(comment)

    db.flush()

    # Registrar comentario en historial
    add_ticket_history(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="comment_added",
        description="Comment added to ticket",
    )

    # Si alguien distinto del creador comenta,
    # notificamos al creador del ticket.
    if current_user.id != ticket.created_by:
        create_notification(
            db=db,
            user_id=ticket.created_by,
            ticket_id=ticket.id,
            title="New comment",
            message=f"New comment added to ticket #{ticket.id}.",
        )

    db.commit()
    db.refresh(comment)

    return comment


@router.get(
    "/{ticket_id}/comments",
    response_model=list[CommentResponse],
)
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if (
        current_user.role == "employee"
        and ticket.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view these comments",
        )

    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.id.asc())
        .all()
    )