from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.permissions import require_roles
from app.models.ticket import Ticket
from app.models.user import User


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "support")
    ),
):
    active_tickets = db.query(Ticket).filter(
        Ticket.deleted_at.is_(None)
    )

    total = active_tickets.count()

    open_tickets = (
        active_tickets
        .filter(Ticket.status == "open")
        .count()
    )

    in_progress = (
        active_tickets
        .filter(Ticket.status == "in_progress")
        .count()
    )

    resolved = (
        active_tickets
        .filter(Ticket.status == "resolved")
        .count()
    )

    closed = (
        active_tickets
        .filter(Ticket.status == "closed")
        .count()
    )

    unassigned = (
        active_tickets
        .filter(Ticket.assigned_to.is_(None))
        .count()
    )

    high_priority = (
        active_tickets
        .filter(Ticket.priority == "high")
        .count()
    )

    return {
        "total_tickets": total,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress,
        "resolved_tickets": resolved,
        "closed_tickets": closed,
        "unassigned_tickets": unassigned,
        "high_priority_tickets": high_priority,
    }