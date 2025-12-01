from services import get_weather_by_coords, get_weather_by_bairro, list_bairros

def test_integration_open_meteo_coords():
    ok, data = get_weather_by_coords("-25.487", "-52.53")
    assert isinstance(ok, bool)
    assert isinstance(data, dict)

def test_integration_open_meteo_bairro():
    bairros = list_bairros()
    assert len(bairros) > 0
    nome = bairros[0]["bairro"]
    ok, data = get_weather_by_bairro(nome)
    assert isinstance(ok, bool)
    assert isinstance(data, dict)
