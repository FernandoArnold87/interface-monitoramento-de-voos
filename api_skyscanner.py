import os
import httpx
from datetime import datetime

async def buscar_voos_skyscanner(origem, destino, data_partida, data_retorno):
    try:
        # Conversão de datas para o formato ISO (YYYY-MM-DD)
        data_partida = datetime.strptime(data_partida, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_retorno = datetime.strptime(data_retorno, "%d/%m/%Y").strftime("%Y-%m-%d")

        url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"  # Exemplo de endpoint correto
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY_SKYSCANNER"),
            "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
        }
        params = {
            "from": origem.upper(),
            "to": destino.upper(),
            "departureDate": data_partida,
            "returnDate": data_retorno,
            "adults": 1,
            "currency": "EUR"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

        voos = []
        for v in data.get("data", []):
            voos.append({
                "origem": origem,
                "destino": destino,
                "data_partida": data_partida,
                "data_retorno": data_retorno,
                "preco": f"{v.get('price', 'N/A')} EUR",
                "link": v.get("link", "#")
            })

        return voos

    except Exception as e:
        print(f"[SKYSCANNER] Erro: {e}")
        return []

