import requests
import json

hackathon_url = "https://hackathon-1pvb.onrender.com/api/ai-model/v2/chat"

API_KEY = "sk_aa4acf97125202714c9288db1e0dc176870708e4"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
    "Referer": "https://hackathon-1pvb.onrender.com",
    "Origin": "https://hackathon-1pvb.onrender.com"

}

def generate_flashcards(topic, amount=5, level="General"):
    prompt = f"""
Eres un asistente educativo experto.

Crea {amount} tarjetas sobre: {topic}.
Nivel: {level}.

Devuelve SOLO JSON en este formato:

[
  {{
    "Pregunta": "...",
    "Respuesta": "...",
    "Dificultad": "{level}"
  }}
]
"""

    payload = {
        "context": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            hackathon_url,
            headers=headers,
            json=payload,
            timeout=120
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        response.raise_for_status()

        result = response.json()
        ai_text = result.get("prompt", "")

        # Extract JSON from the response
        start = ai_text.find('[')
        end = ai_text.rfind(']') + 1
        if start != -1 and end != -1:
            json_str = ai_text[start:end]
            return json.loads(json_str)
        else:
            return [{"Pregunta": "Error", "Respuesta": "No JSON found", "Dificultad": level}]

    except Exception as e:
        print("ERROR:", e)

        return [
            {
                "Pregunta": "Error",
                "Respuesta": str(e),
                "Dificultad": level
            }
        ]

# Test the function
result = generate_flashcards("Python basics", 2, "Beginner")
print("Result:", result)