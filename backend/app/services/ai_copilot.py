import os

from openai import OpenAI
from sqlalchemy.orm import Session

from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage
from app.services.knowledge_service import search_knowledge


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def chat_with_copilot(
    db: Session,
    user_id: int,
    conversation_id: int | None,
    message: str,
):

    # 1. Crear o recuperar conversación

    if conversation_id is None:

        conversation = AIConversation(
            user_id=user_id,
            title=message[:100],
        )

        db.add(conversation)
        db.flush()

    else:

        conversation = (
            db.query(AIConversation)
            .filter(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise ValueError(
                "Conversation not found"
            )

    # 2. Guardar mensaje del usuario

    user_message = AIMessage(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )

    db.add(user_message)
    db.flush()

    # 3. Buscar información relevante en RAG

    chunks = search_knowledge(
        db=db,
        query=message,
        limit=5,
    )

    context = "\n\n".join(
    [
        (
            f"Documento: {result['chunk'].document_name}\n"
            f"Contenido: {result['chunk'].content}"
        )
        for result in chunks
    ]
)

    # 4. Recuperar conversación anterior

    previous_messages = (
        db.query(AIMessage)
        .filter(
            AIMessage.conversation_id == conversation.id
        )
        .order_by(AIMessage.created_at.asc())
        .all()
    )

    messages = []

    for previous_message in previous_messages:

        messages.append(
            {
                "role": previous_message.role,
                "content": previous_message.content,
            }
        )

    # 5. Construir instrucciones

    system_prompt = f"""
Eres un copiloto de soporte de TI empresarial.

Tu función es ayudar a los empleados a resolver
problemas relacionados con sistemas, software,
hardware, red, cuentas y acceso.

Utiliza la base de conocimiento proporcionada
cuando sea relevante.

No inventes procedimientos.

Si la información necesaria no está en la base
de conocimiento, dilo claramente.

BASE DE CONOCIMIENTO:

{context}
"""

    # 6. Preguntar a OpenAI

    response = client.responses.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini",
        ),
        instructions=system_prompt,
        input=messages,
    )

    answer = response.output_text

    # 7. Guardar respuesta

    assistant_message = AIMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
    )

    db.add(assistant_message)

    db.commit()

    return {
        "conversation_id": conversation.id,
        "question": message,
        "answer": answer,
        "sources": [
    {
        "document": result["chunk"].document_name,
        "content": result["chunk"].content,
        "distance": result["distance"],
    }
    for result in chunks
   ],
 }