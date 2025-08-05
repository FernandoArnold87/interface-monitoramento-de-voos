import httpx
import os

async def buscar_voos_kiwi(origem, destino, data_partida, data_retorno):
    url = "https://kiwi-com.p.rapidapi.com/v2/search"
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY_KIWI"),
        "X-RapidAPI-Host": "kiwi-com.p.rapidapi.com"
    }
    params = {
        "fly_from": origem,
        "fly_to": destino,
        "date_from": data_partida,
        "date_to": data_partida,
        "return_from": data_retorno,
        "return_to": data_retorno,
        "curr": "BRL",
        "limit": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []
        data = response.json().get("data", [])

    voos = []
    for voo in data:
        voos.append({
            "origem": origem,
            "destino": destino,
            "data_partida": voo["local_departure"][:10],
            "data_retorno": data_retorno,
            "preco": f'R${voo["price"]},00',
            "link": voo.get("deep_link", "#")
        })
    return voos
