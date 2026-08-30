from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory
from app.schemas.ticket_history import TicketHistoryResponse


router = APIRouter(
    prefix="/tickets",
    tags=["Ticket History"],
)


@router.get(
    "/{ticket_id}/history",
    response_model=list[TicketHistoryResponse],
)
def get_ticket_history(
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
            detail="You do not have permission to access this history",
        )

    history = (
        db.query(TicketHistory)
        .filter(TicketHistory.ticket_id == ticket_id)
        .order_by(TicketHistory.created_at.asc())
        .all()
    )

    return history