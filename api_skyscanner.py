import os
import httpx

async def buscar_voos_skyscanner(origem, destino, data_partida, data_retorno):
    try:
        url = "https://sky-scanner3.p.rapidapi.com/flights"
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY_SKYSCANNER"),
            "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
        }
        params = {
            "from": origem.upper(),
            "to": destino.upper(),
            "departureDate": data_partida,
            "returnDate": data_retorno,
            "currency": "EUR",
            "adults": "1"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            data = response.json()

        voos = []
        for v in data.get("data", []):
            voos.append({
                "origem": origem,
                "destino": destino,
                "data_partida": data_partida,
                "data_retorno": data_retorno,
                "preco": f"{v['price']} EUR",
                "link": v.get("link", "#")
            })
        return voos
    except Exception as e:
        print(f"[SKYSCANNER] Erro: {e}")
        return []

