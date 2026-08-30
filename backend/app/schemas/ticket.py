from pydantic import BaseModel
from typing import Literal


class TicketCreate(BaseModel):
    title:str
    description:str
    priority:str = "normal"


class TicketResponse(BaseModel):
    id:int
    title:str
    description:str
    status:str
    priority:str

    ai_category: str | None = None

    ai_priority: str | None = None

    ai_summary: str | None = None

    ai_suggested_response: str | None = None

    created_by: int
    assigned_to:int | None

    model_config = {
        "from_attributes": True
    }
    


class TicketUpdate(BaseModel):
    title:str | None = None
    description:str| None = None
    status:Literal[
        "open",
        "in_progress",
        "resolved",
        "closed"
    ] | None = None
    priority:str| None = None
    

class TicketAssign(BaseModel):
    user_id: int


class TicketStatusUpdate(BaseModel):
    status: Literal[
        "open",
        "in_progress",
        "resolved",
        "closed",
    ]


##
## Aquí estamos diciendo:
##
## Cuando alguien cree un ticket:
## {
##  "title": "No funciona el Wi-Fi",
##  "description": "No puedo conectarme a la red institucional",
##  "priority": "high"
## }
##
## El backend lo recibirá mediante: TicketCreate
##
## Y cuando respondamos:  TicketResponse
##