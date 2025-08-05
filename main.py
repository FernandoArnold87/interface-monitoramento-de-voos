from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner
from datetime import datetime

app = FastAPI()

# Pasta para arquivos estáticos (logo, imagens, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pasta com os arquivos HTML
templates = Jinja2Templates(directory="templates")

# Página inicial com o formulário
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota que recebe os dados do formulário e busca voos
@app.post("/precos", response_class=HTMLResponse)
async def precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_partida: str = Form(...),
    data_retorno: str = Form(...)
):
    try:
        # Converter data de dd/mm/yyyy para yyyy-mm-dd
        data_partida_iso = datetime.strptime(data_partida, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_retorno_iso = datetime.strptime(data_retorno, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": "Formato de data inválido. Use DD/MM/AAAA."
        })

    # Buscar voos nas APIs
    voos_kiwi = await buscar_voos_kiwi(origem, destino, data_partida_iso, data_retorno_iso)
    voos_skyscanner = await buscar_voos_skyscanner(origem, destino, data_partida_iso, data_retorno_iso)

    # Combinar resultados
    voos = voos_kiwi + voos_skyscanner

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "voos": voos
    })
