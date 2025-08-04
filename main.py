from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
def precos(request: Request, origem: str = Form(...), destino: str = Form(...), data_ida: str = Form(...)):
    try:
        # Converte data para formato dd/mm/yyyy
        data_formatada = datetime.strptime(data_ida, "%Y-%m-%d").strftime("%d/%m/%Y")
        url = f"https://api.skypicker.com/flights?flyFrom={origem}&to={destino}&dateFrom={data_formatada}&dateTo={data_formatada}&partner=picky"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            voos = dados.get("data", [])
        else:
            voos = []

    except Exception as e:
        voos = []
        print(f"Erro ao buscar voos: {e}")

    return templates.TemplateResponse("resultados.html", {"request": request, "voos": voos})
