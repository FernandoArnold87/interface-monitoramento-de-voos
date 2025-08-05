from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
async def buscar_precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_partida: str = Form(...),
    data_retorno: str = Form(...)
):
    try:
        # Tenta buscar na Kiwi
        voos = await buscar_voos_kiwi(origem, destino, data_partida, data_retorno)

        # Se não encontrar nada, tenta na Skyscanner
        if not voos:
            voos = await buscar_voos_skyscanner(origem, destino, data_partida, data_retorno)

        return templates.TemplateResponse("resultados.html", {"request": request, "voos": voos})
    except Exception as e:
        return templates.TemplateResponse("resultados.html", {"request": request, "voos": [], "erro": str(e)})
