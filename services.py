import requests

# Catálogo simples de bairros de Rio Bonito do Iguaçu com coordenadas aproximadas.
# Ajuste as coordenadas conforme fontes locais. Estes pontos são exemplos próximos à região.
BAIRROS_RIO_BONITO = [
    {"bairro": "Centro", "lat": -25.4870, "lon": -52.5300},
    {"bairro": "Vila Xisto", "lat": -25.4950, "lon": -52.5400},
    {"bairro": "Vila São Pedro", "lat": -25.4800, "lon": -52.5200},
    {"bairro": "Linha Gaúcha", "lat": -25.4700, "lon": -52.5100},
    {"bairro": "Rio Guarani", "lat": -25.5050, "lon": -52.5500},
]

def list_bairros():
    # Lista apenas os nomes para facilitar uso no frontend.
    return [{"bairro": b["bairro"], "lat": b["lat"], "lon": b["lon"]} for b in BAIRROS_RIO_BONITO]

def find_bairro_coords(nome_bairro: str):
    nome_bairro = (nome_bairro or "").strip().lower()
    for b in BAIRROS_RIO_BONITO:
        if b["bairro"].lower() == nome_bairro:
            return b["lat"], b["lon"]
    return None, None

# Integração com API pública Open-Meteo (sem necessidade de chave)
# https://open-meteo.com/
def get_weather_by_coords(lat: str, lon: str):
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=temperature_2m,precipitation,wind_speed_10m"
            "&current=temperature_2m,wind_speed_10m"
            "&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return True, resp.json()
        return False, {"status_code": resp.status_code}
    except Exception as e:
        return False, {"error": str(e)}

def get_weather_by_bairro(bairro: str):
    lat, lon = find_bairro_coords(bairro)
    if lat is None or lon is None:
        return False, {"error": f"Bairro '{bairro}' não encontrado"}
    return get_weather_by_coords(str(lat), str(lon))
