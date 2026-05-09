from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from Cerebro import generate_flashcards

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "Backend funcionando correctamente"}

@app.get("/flashcards")
def get_flashcards(topic: str, amount: int = 5, level: str = "General"):
    return generate_flashcards(topic, amount, level)

@app.post("/generate-flashcards")
def create_flashcards(data: dict):
    topic = data.get("Tema")
    amount = data.get("Cantidad", 5)
    level = data.get("Dificultad", "General")

    amount = max(1, min(amount, 20))

    if not topic:
        return {"error": "El tema de estudio es requerido."}

    flashcards = generate_flashcards(topic, amount, level)

    return {
        "Tema": topic,
        "Cantidad": amount,
        "Dificultad": level,
        "Tarjetas": flashcards
    }

@app.get("/flashcards-page", response_class=HTMLResponse)
def flashcards_page(topic: str, amount: int = 5, level: str = "General"):
    flashcards = generate_flashcards(topic, amount, level)
    
    # Build HTML cards
    cards_html = ""
    for card in flashcards:
        cards_html += f"""
    <div class="caja">
        <div class="flashcard">
            <p>{card.get('pregunta', 'N/A')}</p>
        </div><br><br>
        <div class="respuestaParent flashcard">
            <div class="respuestaChild">
                <p>{card.get('respuesta', 'N/A')}</p>
            </div>
        </div>
    </div>"""
    
    html_content = f"""<!DOCTYPE html>
<html> 
<head>
    <title>Flashcards {topic}</title>
    <style>
        body{{
            background-color: aliceblue;
            text-align: center;
            font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        }}
        .flashcard {{
            width: 300px;
            height: 100px;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 15px 15px;
            text-align: center;
            background-color: white;
        }}
        .respuestaParent:hover .respuestaChild{{
            display: block;
        }}
        .respuestaChild{{
            display: none;
        }}
        .caja{{
            display: flex;
            align-items: center;
            flex-direction: column;
            gap: 10px;
        }}
    </style>
</head>
<body>
    <h1>Flashcards</h1>
    <h2>{topic}</h2>
    <h2>{level}</h2>
    {cards_html}
</body>
</html>"""
    
    return html_content
