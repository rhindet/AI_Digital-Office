from pydantic import BaseModel


class AICopilotRequest(BaseModel):

    conversation_id: int | None = None

    message: str