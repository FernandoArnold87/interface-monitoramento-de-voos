from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from api_kiwi import buscar_voos_kiwi
from api_skyscanner import buscar_voos_skyscanner

app = FastAPI()

# Monta a pasta de arquivos estáticos (imagens, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a pasta de templates HTML
templates = Jinja2Templates(directory="templates")

# Página inicial (formulário de busca)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint que processa o formulário e exibe resultados
@app.post("/precos", response_class=HTMLResponse)
async def precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_partida: str = Form(...),
    data_retorno: str = Form(...)
):
    try:
        # Converte data de "dd/mm/yyyy" para "dd/mm/yyyy" (exigido pela Kiwi e Skyscanner via RapidAPI)
        data_partida_formatada = datetime.strptime(data_partida, "%d/%m/%Y").strftime("%d/%m/%Y")
        data_retorno_formatada = datetime.strptime(data_retorno, "%d/%m/%Y").strftime("%d/%m/%Y")

        # Busca voos em ambas as APIs
        voos_kiwi = await buscar_voos_kiwi(origem, destino, data_partida_formatada, data_retorno_formatada)
        voos_skyscanner = await buscar_voos_skyscanner(origem, destino, data_partida_formatada, data_retorno_formatada)

        # Junta os resultados
        voos = voos_kiwi + voos_skyscanner

        # Debug no console (opcional)
        print("Voos KIWI:", voos_kiwi)
        print("Voos SKYSCANNER:", voos_skyscanner)

        # Renderiza o template com os voos encontrados
        return templates.TemplateResponse("resultados.html", {"request": request, "voos": voos})
    
    except Exception as e:
        print("Erro ao buscar voos:", e)
        return templates.TemplateResponse("resultados.html", {"request": request, "voos": []})
