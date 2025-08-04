from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Montar diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório de templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def formulario(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/precos", response_class=HTMLResponse)
async def buscar_precos(
    request: Request,
    origem: str = Form(...),
    destino: str = Form(...),
    data_ida: str = Form(...),
    data_volta: str = Form(...)
):
    url = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"

    querystring = {
        "source": f"City%3A{origem.upper()}",
        "destination": f"City%3A{destino.upper()}",
        "currency": "usd",
        "locale": "en",
        "adults": "1",
        "children": "0",
        "infants": "0",
        "cabinClass": "ECONOMY",
        "sortBy": "QUALITY",
        "sortOrder": "ASCENDING",
        "applyMixedClasses": "true",
        "allowReturnFromDifferentCity": "true",
        "allowChangeInboundDestination": "true",
        "allowChangeInboundSource": "true",
        "allowDifferentStationConnection": "true",
        "enableSelfTransfer": "true",
        "allowOvernightStopover": "true",
        "enableTrueHiddenCity": "true",
        "enableThrowAwayTicketing": "true",
        "outbound": data_ida,
        "inbound": data_volta,
        "transportTypes": "FLIGHT",
        "limit": "20"
    }

    headers = {
        "X-RapidAPI-Key": "91f14f42abmsh4284770cfc06d62p116ec3jsn2d9b0dc985b7",
        "X-RapidAPI-Host": "kiwi-com-cheap-flights.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if response.status_code != 200 or "items" not in data:
            return templates.TemplateResponse("resultados.html", {
                "request": request,
                "erro": f"Erro ao buscar dados. Código {response.status_code}",
                "voos": []
            })

        voos = data["items"]

        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "voos": voos,
            "erro": None
        })

    except Exception as e:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "erro": f"Erro inesperado: {str(e)}",
            "voos": []
        })
