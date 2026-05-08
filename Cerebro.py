import requests
import json

# Ollama local API
ollama_url = "http://localhost:11434/api/generate"

def generate_flashcards(topic, amount=5, level="General"):

    prompt = f"""
Eres un asistente educativo experto.

Crea {amount} tarjetas de estudio sobre el tema: {topic}.
Nivel: {level}.

Devuelve SOLO JSON en este formato:

[
  {{
    "Pregunta": "Pregunta clara aquí",
    "Respuesta": "Respuesta breve y concisa aquí",
    "Dificultad": "{level}"
  }}
]
"""

    # Payload for Ollama
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            ollama_url,
            json=payload,
            timeout=120
        )

        print("✅ STATUS:", response.status_code)
        print("🔍 RESPONSE:", response.text)

        response.raise_for_status()

        result = response.json()

        # Get the response from Ollama
        ai_text = result.get("response", "")

        # Clean the response (remove code blocks if present)
        ai_text = ai_text.strip("```json").strip("```").strip()

        print("🧠 TEXTO IA:", ai_text)

        try:
            flashcards = json.loads(ai_text)
        except json.JSONDecodeError as e:
            print("❌ ERROR JSON:", e)

            flashcards = [
                {
                    "Pregunta": "Error al convertir JSON",
                    "Respuesta": ai_text,
                    "Dificultad": level
                }
            ]

        return flashcards

    except requests.exceptions.RequestException as e:
        print("❌ ERROR HTTP:", e)

        return [
            {
                "Pregunta": "Error de conexión",
                "Respuesta": str(e),
                "Dificultad": level
            }
        ]
