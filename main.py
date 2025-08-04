from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
async def precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_ida: str = Form(...)
):
    try:
        # Define URLs das APIs
        urls = [
            f"https://api.skypicker.com/flights?flyFrom={origem}&to={destino}&dateFrom={data_ida}&dateTo={data_ida}&partner=picky&curr=EUR&limit=10&sort=price",
            f"https://api.tequila.kiwi.com/v2/search?fly_from={origem}&fly_to={destino}&date_from={data_ida}&date_to={data_ida}&curr=EUR&limit=10&sort=price"
        ]

        headers_kiwi = {
            "apikey": "tequila"  # Para fins educacionais, sem chave oficial
        }

        voos = []

        # Tenta cada API
        for url in urls:
            try:
                if "kiwi.com" in url:
                    response = requests.get(url, headers=headers_kiwi)
                else:
                    response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    resultado = data.get("data", [])
                    if resultado:
                        voos.extend(resultado)
            except Exception:
                continue

        if not voos:
            return templates.TemplateResponse("resultados.html", {
                "request": request,
                "voos": [],
                "erro": "Nenhum resultado encontrado ou erro nas fontes."
            })

        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": voos,
            "erro": None
        })

    except Exception as e:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": f"Erro inesperado: {str(e)}"
        })

# Utilitário para formatar datas
def datetimeformat(value):
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%d/%m/%Y %H:%M')
    except:
        return value

templates.env.filters["datetimeformat"] = datetimeformat
