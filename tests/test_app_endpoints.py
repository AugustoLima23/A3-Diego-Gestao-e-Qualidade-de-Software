import json
from app import app

def client():
    return app.test_client()

def test_cadastrar_local_e_listar():
    c = client()
    payload = {
        "nome": "Bairro Centro",
        "endereco": "Rua X, 123",
        "descricao": "Alagamento e queda de árvore",
        "gravidade": "alta"
    }
    r = c.post("/locais", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 201
    body = r.get_json()
    assert "id" in body

    r_list = c.get("/locais")
    assert r_list.status_code == 200
    locais = r_list.get_json()
    assert any(l["id"] == body["id"] for l in locais)

def test_registrar_ajuda_e_listar():
    c = client()
    payload = {
        "tipo": "oferta",
        "descricao": "Doação de telhas",
        "contato": "whatsapp: (41) 99999-0000",
        "status": "aberta"
    }
    r = c.post("/ajudas", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 201
    ajuda_id = r.get_json()["id"]
    assert isinstance(ajuda_id, int)

    r_list = c.get("/ajudas")
    assert r_list.status_code == 200
    ajudas = r_list.get_json()
    assert any(a["id"] == ajuda_id for a in ajudas)

def test_listar_bairros_e_clima_por_bairro():
    c = client()
    r_bairros = c.get("/bairros")
    assert r_bairros.status_code == 200
    bairros = r_bairros.get_json()
    assert len(bairros) > 0
    nome_bairro = bairros[0]["bairro"]

    r_clima = c.get(f"/publico/clima/bairro?bairro={nome_bairro}")
    assert r_clima.status_code in (200, 404)  # 404 caso API ou bairro falhe

def test_clima_por_coords():
    c = client()
    r = c.get("/publico/clima?lat=-25.487&lon=-52.53")
    assert r.status_code in (200, 502)
