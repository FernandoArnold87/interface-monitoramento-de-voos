from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner
from datetime import datetime
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
async def buscar_precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_partida: str = Form(...),
    data_retorno: str = Form(...)
):
    hoje = datetime.today().date()
    try:
        partida_dt = datetime.strptime(data_partida, "%Y-%m-%d").date()
        retorno_dt = datetime.strptime(data_retorno, "%Y-%m-%d").date()
        if partida_dt < hoje or retorno_dt < hoje:
            raise ValueError("As datas devem ser futuras.")
    except ValueError:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "mensagem": "Datas inválidas. Use datas futuras."
        })

    voos = await buscar_voos_kiwi(origem, destino, data_partida, data_retorno)
    if not voos:
        voos = await buscar_voos_skyscanner(origem, destino, data_partida, data_retorno)

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "voos": voos,
        "origem": origem,
        "destino": destino
    })
