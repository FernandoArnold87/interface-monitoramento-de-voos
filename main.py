from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

# Monta diretório estático e templates
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
    data_ida: str = Form(...),
    data_volta: str = Form(...)
):
    resultados = []

    headers = {
        "X-RapidAPI-Key": "91f14f42abmsh4284770cfc06d62p116ec3jsn2d9b0dc985b7"
    }

    try:
        async with httpx.AsyncClient() as client:
            # API 1
            url1 = "https://flight-data28.p.rapidapi.com/flights/search/summary"
            params1 = {
                "fly_from": origem.upper(),
                "fly_to": destino.upper(),
                "date_from": data_ida,
                "date_to": data_volta,
                "curr": "EUR",
                "limit": 10
            }
            headers1 = headers.copy()
            headers1["X-RapidAPI-Host"] = "flight-data28.p.rapidapi.com"
            res1 = await client.get(url1, params=params1, headers=headers1)
            if res1.status_code == 200:
                dados1 = res1.json()
                resultados.append({"fonte": "Flight-Data28", "dados": dados1.get("data", [])})
            else:
                resultados.append({"fonte": "Flight-Data28", "erro": f"Código {res1.status_code}"})

            # API 2
            url2 = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"
            params2 = {
                "source": f"City:{origem}",
                "destination": f"City:{destino}",
                "dateFrom": data_ida,
                "dateTo": data_volta,
                "currency": "eur",
                "limit": 10
            }
            headers2 = headers.copy()
            headers2["X-RapidAPI-Host"] = "kiwi-com-cheap-flights.p.rapidapi.com"
            res2 = await client.get(url2, params=params2, headers=headers2)
            if res2.status_code == 200:
                dados2 = res2.json()
                resultados.append({"fonte": "Kiwi", "dados": dados2})
            else:
                resultados.append({"fonte": "Kiwi", "erro": f"Código {res2.status_code}"})

    except Exception as e:
        return templates.TemplateResponse("resultados.html", {
            "request": request,
            "erro": str(e),
            "resultados": []
        })

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "resultados": resultados
    })
