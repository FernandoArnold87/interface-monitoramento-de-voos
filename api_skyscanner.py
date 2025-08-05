import httpx
import os

async def buscar_voos_skyscanner(origem, destino, data_partida, data_retorno):
    url = "https://fly-scraper.p.rapidapi.com/flights/search-detail"
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY_SKYSCANNER"),
        "X-RapidAPI-Host": "fly-scraper.p.rapidapi.com"
    }
    body = {
        "market": "US",
        "locale": "en-US",
        "currency": "USD",
        "cabinClass": "economy",
        "adults": 1,
        "childrenAges": [],
        "itineraryType": "ROUND",
        "legs": [
            {"origin": origem, "destination": destino, "date": data_partida},
            {"origin": destino, "destination": origem, "date": data_retorno}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body, headers=headers)
        if response.status_code != 200:
            return []
        data = response.json()

    voos = []
    for item in data.get("data", [])[:10]:
        voos.append({
            "origem": origem,
            "destino": destino,
            "data_partida": data_partida,
            "data_retorno": data_retorno,
            "preco": item.get("price", "N/A"),
            "link": item.get("deeplink", "#")
        })
    return voos
