# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI()

# Diretórios
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Sua chave da API RapidAPI para Kiwi
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or "SUA_CHAVE_AQUI"

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
    url = "https://kiwi-com.p.rapidapi.com/v2/search"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "kiwi-com.p.rapidapi.com"
    }

    params = {
        "fly_from": origem.upper(),
        "fly_to": destino.upper(),
        "date_from": data_partida,
        "date_to": data_partida,
        "return_from": data_retorno,
        "return_to": data_retorno,
        "curr": "BRL",
        "limit": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        dados = response.json()

    voos = dados.get("data", [])

    return templates.TemplateResponse("resultados.html", {
        "request": request,
        "voos": voos,
        "origem": origem,
        "destino": destino
    })
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
