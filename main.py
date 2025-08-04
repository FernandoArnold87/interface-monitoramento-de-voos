from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
def precos(request: Request, origem: str = Form(...), destino: str = Form(...), data_ida: str = Form(...)):
    url = (
        f"https://api.skypicker.com/flights?"
        f"flyFrom={origem}&to={destino}&dateFrom={data_ida}&dateTo={data_ida}"
        f"&partner=picky&curr=EUR&limit=5&sort=price"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": f"Erro ao buscar dados. Código {response.status_code}"
        })

    try:
        dados = response.json()
        voos = dados.get("data", [])
    except ValueError:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": [],
            "erro": "Resposta inválida da API."
        })

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "voos": voos,
        "erro": None
    })

# Filtro para formatar timestamps da API
def datetimeformat(value):
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%d/%m/%Y %H:%M')
    except:
        return "-"

templates.env.filters["datetimeformat"] = datetimeformat

