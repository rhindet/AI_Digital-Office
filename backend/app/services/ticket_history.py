from sqlalchemy.orm import Session

from app.models.ticket_history import TicketHistory

def add_ticket_history(
        db:Session,
        ticket_id:int,
        user_id:int,
        action:str,
        description:str | None = None,
):
    history = TicketHistory(
        ticket_id = ticket_id,
        user_id=user_id,
        action=action,
        description=description
    )

    db.add(history)