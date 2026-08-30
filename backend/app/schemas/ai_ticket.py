from pydantic import BaseModel
from typing import Literal


class AITicketAnalysis(BaseModel):
    category: Literal[
        "hardware",
        "software",
        "network",
        "access",
        "account",
        "other",
    ]

    priority: Literal[
        "low",
        "normal",
        "high",
    ]

    summary: str

    suggested_response: str