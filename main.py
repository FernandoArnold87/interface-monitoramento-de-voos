from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner
from datetime import datetime

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
        # Converter datas do formato do HTML para o formato DD/MM/YYYY
        data_partida_convertida = datetime.strptime(data_partida, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_retorno_convertida = datetime.strptime(data_retorno, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": "Formato de data inválido. Use DD/MM/AAAA."
        })

    voos_kiwi = await buscar_voos_kiwi(origem, destino, data_partida_convertida, data_retorno_convertida)
    voos_skyscanner = await buscar_voos_skyscanner(origem, destino, data_partida_convertida, data_retorno_convertida)

    voos = voos_kiwi + voos_skyscanner
    return templates.TemplateResponse("resultados.html", {"request": request, "voos": voos})

