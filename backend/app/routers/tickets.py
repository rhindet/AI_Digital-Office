from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.ticket import Ticket
from app.models.user import User

from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketUpdate,
    TicketAssign,
    TicketStatusUpdate,
)

from app.core.dependencies import get_current_user
from app.core.permissions import require_roles

from app.services.ticket_history import add_ticket_history
from app.services.notifications import create_notification
from app.services.ai_ticket import analyze_ticket
from app.services.ticket_assignment import assign_ticket_automatically


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "/",
    response_model=TicketResponse,
)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Crear el ticket inicialmente
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status="open",
        created_by=current_user.id,
    )

    db.add(new_ticket)

    # Necesitamos el ID antes de crear el historial
    db.flush()

    # 2. Analizar el ticket con IA
    ai_result = await analyze_ticket(
        new_ticket.title,
        new_ticket.description,
    )

    new_ticket.ai_category = ai_result.category
    new_ticket.ai_priority = ai_result.priority
    new_ticket.ai_summary = ai_result.summary
    new_ticket.ai_suggested_response = ai_result.suggested_response

        # 3. Aplicar la prioridad determinada por la IA
    ai_priority = ai_result.priority

    if ai_priority in ["low", "normal", "high"]:
        new_ticket.priority = ai_priority

    # 4. Asignar automáticamente el ticket
    assigned_user = assign_ticket_automatically(
        db=db,
        ticket=new_ticket,
    )

    # 5. Crear historial de creación
    add_ticket_history(
        db=db,
        ticket_id=new_ticket.id,
        user_id=current_user.id,
        action="created",
        description="Ticket created",
    )

    # 6. Registrar la asignación automática
    if assigned_user:
        add_ticket_history(
            db=db,
            ticket_id=new_ticket.id,
            user_id=current_user.id,
            action="assigned",
            description=(
                f"Ticket automatically assigned to "
                f"user {assigned_user.id}"
            ),
        )

        # 7. Notificar al soporte
        create_notification(
            db=db,
            user_id=assigned_user.id,
            ticket_id=new_ticket.id,
            title="New ticket assigned",
            message=(
                f"Ticket #{new_ticket.id} has been "
                f"automatically assigned to you."
            ),
        )

    # 8. Guardar todos los cambios
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get(
    "/",
    response_model=list[TicketResponse],
)
def get_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role in ["admin", "support"]:
        tickets = (
            db.query(Ticket)
            .filter(Ticket.deleted_at.is_(None))
            .all()
        )
    else:
        tickets = (
            db.query(Ticket)
            .filter(
                Ticket.created_by == current_user.id,
                Ticket.deleted_at.is_(None),
            )
            .all()
        )

    return tickets


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.deleted_at.is_(None),
        )
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
            detail="You do not have permission to access this ticket",
        )

    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.deleted_at.is_(None),
        )
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
            detail="You do not have permission to modify this ticket",
        )

    update_data = ticket_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(ticket, field, value)

    add_ticket_history(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="updated",
        description="Ticket updated",
    )

    db.commit()
    db.refresh(ticket)

    return ticket


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "support")
    ),
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

    ticket.deleted_at = datetime.utcnow()

    add_ticket_history(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="deleted",
        description="Ticket deleted",
    )

    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }


@router.patch(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket(
    ticket_id: int,
    data: TicketAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "support")
    ),
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.deleted_at.is_(None),
        )
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    previous_assignee = ticket.assigned_to

    ticket.assigned_to = user.id

    add_ticket_history(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="assigned",
        description=(
            f"Ticket reassigned from "
            f"{previous_assignee} to {user.id}"
        ),
    )

    create_notification(
        db=db,
        user_id=user.id,
        ticket_id=ticket.id,
        title="Ticket assigned",
        message=f"Ticket #{ticket.id} has been assigned to you.",
    )

    db.commit()
    db.refresh(ticket)

    return ticket


@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
)
def update_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "support")
    ),
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.deleted_at.is_(None),
        )
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    if status_data.status is None:
        raise HTTPException(
            status_code=400,
            detail="Status is required",
        )

    old_status = ticket.status

    ticket.status = status_data.status

    add_ticket_history(
        db=db,
        ticket_id=ticket.id,
        user_id=current_user.id,
        action="status_changed",
        description=(
            f"Status changed from "
            f"{old_status} to {ticket.status}"
        ),
    )

    create_notification(
        db=db,
        user_id=ticket.created_by,
        ticket_id=ticket.id,
        title="Ticket status changed",
        message=(
            f"Ticket #{ticket.id} status changed "
            f"to {ticket.status}."
        ),
    )

    db.commit()
    db.refresh(ticket)

    return ticket