import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

hackathon_url = "https://hackathon-1pvb.onrender.com/api/ai-model/v2/chat"

API_KEY= "sk_addb0a2a0eda93bb4b79be89b177b1b48f7535f9"

headers = {
    "API_KEY":API_KEY,
    "Content-Type": "application/json",
    "Referer": "https://hackathon-1pvb.onrender.com",
    "Origin": "https://hackathon-1pvb.onrender.com"
}

def generate_flashcards(topic, amount=5, level="General"):
    prompt = f"""
Eres un asistente educativo experto.

Crea {amount} tarjetas de estudio sobre el tema: {topic}.
Nivel de dificultad: {level}.

Responde solamente en formato JSON válido.
No escribas explicación fuera del JSON.

Usa esta estructura exactamente para cada tarjeta:

[
  {{
    "Pregunta": "Pregunta clara aquí",
    "Respuesta": "Respuesta breve y concisa aquí",
    "Dificultad": "{level}"
  }}
]
"""

    payload = {
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            hackathon_url,
            headers=headers,
            json=payload,
            timeout=120
        )

        print("Status:", response.status_code)
        print("Raw:", response.text)

        response.raise_for_status()

        result = response.json()

        ai_text = result.get("response", "")

        try:
            flashcards = json.loads(ai_text)
        except json.JSONDecodeError:
            flashcards = [
                {
                    "Pregunta": "Error al convertir la respuesta en JSON",
                    "Respuesta": ai_text,
                    "Dificultad": level
                }
            ]

        return flashcards

    except requests.exceptions.RequestException as e:
        return [
            {
                "Pregunta": "Error de conexión con la API",
                "Respuesta": str(e),
                "Dificultad": level
            }
        ]


# Prueba
if __name__ == "__main__":
    cards = generate_flashcards("Fotosíntesis", amount=5, level="Fácil")

    print(json.dumps(cards, indent=4, ensure_ascii=False))
