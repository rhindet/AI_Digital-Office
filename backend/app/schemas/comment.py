from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    ticket_id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }