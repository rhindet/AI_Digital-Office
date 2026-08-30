from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User


def assign_ticket_automatically(
    db: Session,
    ticket: Ticket,
) -> User | None:

    # Buscar soporte activo especializado
    # en la categoría detectada por la IA.
    support_user = (
        db.query(User)
        .filter(
            User.role == "support",
            User.support_category == ticket.ai_category,
            User.is_active.is_(True),
        )
        .first()
    )

    if support_user is None:
        return None

    ticket.assigned_to = support_user.id

    return support_user