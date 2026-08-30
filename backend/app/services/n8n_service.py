import os
import httpx


N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "http://localhost:5678/webhook/ai-office",
)


async def send_to_n8n(
    event: str,
    data: dict,
):
    payload = {
        "event": event,
        "data": data,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:

        print("Se llamo")

        response = await client.post(
            N8N_WEBHOOK_URL,
            json=payload,
        )

        print("Respuesta", response.content)


        response.raise_for_status()

        print("N8N STATUS:", response.status_code)
        print("N8N HEADERS:", response.headers)
        print("N8N TEXT:", repr(response.text))

        if not response.content:
            return {
                "status_code": response.status_code,
                "response": None,
            }

        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            return response.json()

        return {
            "status_code": response.status_code,
            "response": response.text,
        }