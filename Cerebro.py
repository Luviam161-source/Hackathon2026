from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def generate_flashcards(topic, amount=1, level="General"):
    prompt = (
        f"Generate {amount} flashcard about {topic} at a {level} level. "
        f"Return ONLY a JSON object with this structure: "
        f"{{\"flashcards\": [{{ \"pregunta\": \"...\", \"respuesta\": \"...\", \"Dificultad\": \"{level}\" }}]}}"
    )

    payload = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=120)
        if response.status_code == 200:
            raw_ai_text = response.json().get("response", "").strip()
            if "{" in raw_ai_text:
                start = raw_ai_text.find("{")
                end = raw_ai_text.rfind("}") + 1
                data = json.loads(raw_ai_text[start:end])
                return data.get("flashcards", [])
    except Exception as e:
        print(f"Connection Error: {e}")
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    topic = "Python Programming"
    level = "General" # Default
    
    if request.method == 'POST':
        topic = request.form.get('user_topic')
        level = request.form.get('user_level') # Now grabs from the dropdown

    flashcards = generate_flashcards(topic, level=level)
    first_card = flashcards[0] if flashcards else {}

    return render_template('index.html',
                           topic=topic,
                           level=level,
                           pregunta=first_card.get('pregunta', 'No card generated'),
                           respuesta=first_card.get('respuesta', 'Please try again'))

if __name__ == "__main__":
    app.run(debug=True)