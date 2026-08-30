import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.ai_ticket import AITicketAnalysis


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not configured")


client = OpenAI(api_key=api_key)


async def analyze_ticket(
    title: str,
    description: str,
) -> AITicketAnalysis:

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte de TI empresarial. "
                    "Analiza el ticket y devuelve exclusivamente JSON válido. "
                    "No agregues markdown ni texto fuera del JSON. "
                    "Los campos obligatorios son: category, priority, "
                    "summary, suggested_response. "
                    "category debe ser uno de: hardware, software, "
                    "network, access, account, other. "
                    "priority debe ser uno de: low, normal, high. "
                    "summary debe ser un resumen breve en español. "
                    "suggested_response debe ser una respuesta profesional "
                    "y breve en español para el empleado."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Título: {title}\n"
                    f"Descripción: {description}"
                ),
            },
        ],
    )

    try:
        result = json.loads(response.output_text)

        return AITicketAnalysis.model_validate(result)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "OpenAI returned invalid JSON"
        ) from exc