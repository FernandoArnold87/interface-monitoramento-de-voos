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
    url = f"https://api.skypicker.com/flights?flyFrom={origem}&to={destino}&dateFrom={data_ida}&dateTo={data_ida}&partner=picky"
    response = requests.get(url).json()
    voos = response.get("data", [])
    return templates.TemplateResponse("resultados.html", {"request": request, "voos": voos})
