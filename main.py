
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
async def precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_partida: str = Form(...),
    data_retorno: str = Form(...)
):
    try:
        # Corrige o formato para YYYY-MM-DD se necessário pelas APIs
        data_partida_formatada = datetime.strptime(data_partida, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_retorno_formatada = datetime.strptime(data_retorno, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": "Formato de data inválido. Use DD/MM/AAAA."
        })

    voos_kiwi = await buscar_voos_kiwi(origem, destino, data_partida_formatada, data_retorno_formatada)
    voos_skyscanner = await buscar_voos_skyscanner(origem, destino, data_partida_formatada, data_retorno_formatada)

    voos = voos_kiwi + voos_skyscanner

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "voos": voos
    })
