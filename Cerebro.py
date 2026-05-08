import requests
import json 
OLLAMA_URL ="http://Localhost:11434/api/generate"
MODEL_NAME = "llama3.2" 
def generate_flashcards(topic, amount=5, level="General"):
    prompt = f""" 
Eres Un Asistente Educativo Experto.

Crea {amount} tarjetas de estudio sobre el tema : {topic}.
Nivel de dificultad: {level}.

Responde solamente en formato JSON Valido.
No escribas la explicacion fuera del JSON.

Usa esta estructura exactamente para cada tarjeta:
[
  {{
    "Pregunta" : "Pregunta Clara aqui ",
    "Respuesta": "Respuesta Breve y concisa aqui",
    "Dificultad": "{level}" 
    }}
    ]
    """
    response =requests.post(OLLAMA_URL,json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False ,
        "format": "json"
    },
    timeout=120
    )
    response.raise_for_status()

    result = response.json()
    ai_text = result.get("response","")

    try:
        flashcards = json.loads(ai_text)
    except json.JSONDecodeError:
        flashcards = [
            {
                "Pregunta": "Error al generar la tarjeta",
                "Respuesta": ai_text,
                "Dificultad": level
            }
        ]
    return flashcards