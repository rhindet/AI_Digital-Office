from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default="employee"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    # Tickets que creó

    tickets = relationship(

        "Ticket",

        foreign_keys="Ticket.created_by",

        back_populates="creator",

    )

    comments = relationship(
        "Comment",
        back_populates="user",
    )

    assigned_tickets = relationship(

        "Ticket",

        foreign_keys="Ticket.assigned_to",

        back_populates="assignee",

    )
    
    support_category = Column(
        String(50),
        nullable=True
    )

    ai_conversations = relationship(
    "AIConversation",
    back_populates="user",
    cascade="all, delete-orphan",
)

# User
# │
# ├── tickets
# │     └── Tickets que este usuario CREÓ
# │
# ├── assigned_tickets
# │     └── Tickets que tiene ASIGNADOS
# │
# └── comments
#       └── Comentarios que escribió