from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
