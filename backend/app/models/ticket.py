from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="open",
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="normal",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
    nullable=True,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    creator = relationship(

        "User",

        foreign_keys=[created_by],

        back_populates="tickets",

    )

    # Usuario de soporte asignado

    assigned_to: Mapped[int | None] = mapped_column(

        ForeignKey("users.id"),

        nullable=True,

    )

    assignee = relationship(

        "User",

        foreign_keys=[assigned_to],

        back_populates="assigned_tickets",

    )

    comments = relationship(
    "Comment",
    back_populates="ticket",
    cascade="all, delete-orphan",


)

    history = relationship(
    "TicketHistory",
    back_populates="ticket",
)

    ai_category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    ai_priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    ai_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ai_suggested_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


#    Ticket
#  │
#  ├── creator
#  │     └── User que lo creó
#  │
#  ├── assignee
#  │     └── User que lo está atendiendo
#  │
#  └── comments
#        └── Comentarios