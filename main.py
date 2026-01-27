from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# --- IMPORTANTE: Configuración CORS ---
# Permite que el HTML local se conecte con el servidor Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga del modelo (Variable Global)
modelo = pipeline("question-answering", model="deepset/tinyroberta-squad2")


class Consulta(BaseModel):
    pregunta: str
    contexto :str

@app.post("/consulta/")
async def respuesta(datos: Consulta):
    resultado = modelo(question = datos.pregunta, context = datos.contexto)

    print('////////////////77',resultado,'/////////////////////')

    return{
        "respuesta": resultado["answer"],
        "score": round(resultado["score"], 4),
        "inicio": resultado["start"],
        "fin": resultado["end"]
        }