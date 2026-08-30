from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.ticket import Ticket
from app.models.user import User

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/powerbi/tickets")
def powerbi_tickets(db: Session = Depends(get_db)):

    tickets = (
        db.query(
            Ticket.id,
            Ticket.title,
            Ticket.description,
            Ticket.status,
            Ticket.priority,
            Ticket.created_by,
            User.name.label("user_name"),
        )
        .join(
            User,
            Ticket.created_by == User.id
        )
        .all()
    )

    return [
        {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_by": ticket.created_by,
            "user_name": ticket.user_name,
        }
        for ticket in tickets
    ]