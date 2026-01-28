from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from fastapi.responses import FileResponse 


app = FastAPI()

# Permite que el HTML local se conecte con el servidor Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#
from fastapi.staticfiles import StaticFiles
#Sive para permitirle el acceso a acceder a los archivos de la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carga del modelo (Variable Global)
modelo = pipeline("question-answering", model="deepset/tinyroberta-squad2")


class Consulta(BaseModel):
    pregunta: str
    contexto :str


@app.get("/")
def index():
    return FileResponse('static/index.html')


@app.post("/consulta/")
async def respuesta(datos: Consulta):
    resultado = modelo(question = datos.pregunta, context = datos.contexto)

    return{
        "respuesta": resultado["answer"],
        "score": round(resultado["score"], 4),
        "inicio": resultado["start"],
        "fin": resultado["end"]
        }
