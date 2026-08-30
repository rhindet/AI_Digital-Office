from sqlalchemy.orm import Session
from openai import OpenAI
import os

from app.models.knowledge import KnowledgeChunk
from app.services.embedding_service import create_embedding


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Qué tan parecida debe ser la información
# para considerarla relevante.
MAX_DISTANCE = 0.45


def search_knowledge(
    db: Session,
    query: str,
    limit: int = 5,
):
    query_embedding = create_embedding(query)

    results = (
        db.query(
            KnowledgeChunk,
            KnowledgeChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance"),
        )
        .order_by(
            KnowledgeChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(limit)
        .all()
    )

    relevant_chunks = []

    for chunk, distance in results:

        if distance <= MAX_DISTANCE:

            relevant_chunks.append(
                {
                    "chunk": chunk,
                    "distance": float(distance),
                }
            )

    return relevant_chunks





async def ask_knowledge_base(
    db: Session,
    question: str,
):

    # 1. Buscar información relevante
    results = search_knowledge(
        db=db,
        query=question,
        limit=5,
    )

    # 2. Si no encontramos información suficientemente
    # relevante, no preguntamos a OpenAI.
    if not results:

        return {
            "question": question,
            "answer": (
                "No encontré información suficientemente "
                "relevante en la base de conocimiento."
            ),
            "sources": [],
        }

    # 3. Extraer los chunks
    chunks = [
        result["chunk"]
        for result in results
    ]

    # 4. Construir contexto
    context = "\n\n".join(
        [
            f"Documento: {chunk.document_name}\n"
            f"Contenido: {chunk.content}"
            for chunk in chunks
        ]
    )

    # 5. Preguntar a la IA
    response = client.responses.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini"
        ),
        input=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte de TI empresarial. "

                    "Responde utilizando exclusivamente "
                    "la información proporcionada en el contexto. "

                    "No inventes información, procedimientos, "
                    "configuraciones ni pasos que no aparezcan "
                    "en el contexto. "

                    "Si el contexto no contiene información "
                    "suficiente para responder, dilo claramente. "

                    "Responde en español. "

                    "Sé claro, directo y profesional."
                ),
            },
            {
                "role": "user",
                "content": (
                    "CONTEXTO DE LA BASE DE CONOCIMIENTO:\n\n"
                    f"{context}\n\n"

                    "PREGUNTA DEL EMPLEADO:\n"
                    f"{question}"
                ),
            },
        ],
    )

    # 6. Devolver respuesta y fuentes
    return {
        "question": question,

        "answer": response.output_text,

        "sources": [
            {
                "document": chunk.document_name,
                "content": chunk.content,
                "distance": result["distance"],
            }
            for result in results
            for chunk in [result["chunk"]]
        ],
    }