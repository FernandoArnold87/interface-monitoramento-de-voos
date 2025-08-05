import os
import httpx
from datetime import datetime

async def buscar_voos_kiwi(origem, destino, data_partida, data_retorno):
    try:
        # Converte datas para formato YYYY-MM-DD exigido pela API
        data_partida = datetime.strptime(data_partida, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_retorno = datetime.strptime(data_retorno, "%d/%m/%Y").strftime("%Y-%m-%d")

        url = "https://kiwi-com1.p.rapidapi.com/api/v1/flights"

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY_KIWI"),
            "X-RapidAPI-Host": "kiwi-com1.p.rapidapi.com"
        }

        params = {
            "fly_from": origem.upper(),
            "fly_to": destino.upper(),
            "date_from": data_partida,
            "date_to": data_partida,
            "return_from": data_retorno,
            "return_to": data_retorno,
            "curr": "EUR",
            "limit": 5
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
                "preco": f"{v['price']} EUR",
                "link": v.get("deep_link", "#")
            })

        return voos

    except Exception as e:
        print(f"[KIWI] Erro: {e}")
        return []

