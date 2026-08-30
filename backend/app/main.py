from fastapi import FastAPI
from app.database.database import engine
from app.models.base import Base
from app.models.ticket import Ticket
from app.routers.tickets import router as tickets_router

from app.models.comment import Comment
from app.models.user import User

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.comments import router as comments_router
from app.models.ticket_history import TicketHistory
from app.routers.ticket_history import router as ticket_history_router
from app.models.notification import Notification
from app.routers.notifications import router as notifications_router
from app.routers.dashboard import router as dashboard_router

from app.models.knowledge import KnowledgeChunk
from app.routers.knowledge import router as knowledge_router
from fastapi.middleware.cors import CORSMiddleware


from app.routers.ai_copilot import router as ai_copilot_router

from app.routers.analytics import router as analytics_router

from app.services.n8n_service import send_to_n8n

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Digital Office API",
    description="API institucional de IA, automatización y soporte TI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tickets_router) 
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(comments_router)
app.include_router(ticket_history_router)
app.include_router(notifications_router)
app.include_router(dashboard_router)
app.include_router(knowledge_router)
app.include_router(
    ai_copilot_router
)
app.include_router(
    analytics_router
)

@app.post("/test/n8n")
async def test_n8n():

    result = await send_to_n8n(
        event="test",
        data={
            "message": "Hola desde FastAPI",
        },
    ) 

    return result

@app.get("/") 
def root():
    return{
        "application":"AI Digital Office",
        "status":"running",
    } 

@app.get("/health") 
def health():
    return{
        "status":"ok"
    }