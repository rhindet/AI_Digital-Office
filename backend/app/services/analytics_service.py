from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ticket import Ticket
from app.models.user import User


def get_support_metrics(db: Session):

    # -------------------------
    # TOTAL DE TICKETS
    # -------------------------

    total_tickets = (
        db.query(func.count(Ticket.id))
        .scalar()
    )

    # -------------------------
    # TICKETS ABIERTOS
    # -------------------------

    open_tickets = (
        db.query(func.count(Ticket.id))
        .filter(Ticket.status == "open")
        .scalar()
    )

    # -------------------------
    # TICKETS RESUELTOS
    # -------------------------

    resolved_tickets = (
        db.query(func.count(Ticket.id))
        .filter(Ticket.status == "resolved")
        .scalar()
    )

    # -------------------------
    # TICKETS POR PRIORIDAD
    # -------------------------

    tickets_by_priority = (
        db.query(
            Ticket.priority,
            func.count(Ticket.id)
        )
        .group_by(Ticket.priority)
        .all()
    )

    # -------------------------
    # TICKETS POR ESTADO
    # -------------------------

    tickets_by_status = (
        db.query(
            Ticket.status,
            func.count(Ticket.id)
        )
        .group_by(Ticket.status)
        .all()
    )

    # -------------------------
    # TICKETS POR USUARIO
    # -------------------------

    tickets_by_user = (
        db.query(
            User.name,
            func.count(Ticket.id)
        )
        .join(
            Ticket,
            Ticket.created_by == User.id
        )
        .group_by(User.name)
        .all()
    )

    return {

        "total_tickets": total_tickets or 0,

        "open_tickets": open_tickets or 0,

        "resolved_tickets": resolved_tickets or 0,

        "tickets_by_priority": [
            {
                "priority": priority,
                "count": count,
            }
            for priority, count in tickets_by_priority
        ],

        "tickets_by_status": [
            {
                "status": status,
                "count": count,
            }
            for status, count in tickets_by_status
        ],

        "tickets_by_user": [
            {
                "user": name,
                "count": count,
            }
            for name, count in tickets_by_user
        ],
    }