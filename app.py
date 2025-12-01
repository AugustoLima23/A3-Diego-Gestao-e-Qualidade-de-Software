from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, create_local, list_locais, create_ajuda, list_ajudas
from services import get_weather_by_coords, get_weather_by_bairro, list_bairros

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados (SQLite)
init_db()

@app.route("/")
def home():
    return "<h1>API Reconstrução Rio Bonito está rodando!</h1><p>Use /locais, /ajudas, /bairros, /publico/clima, /publico/clima/bairro</p>"

# Cadastro de locais afetados
@app.route("/locais", methods=["POST"])
def cadastrar_local():
    data = request.get_json() or {}
    required = ["nome", "endereco", "descricao", "gravidade"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

    local_id = create_local(
        nome=data["nome"],
        endereco=data["endereco"],
        descricao=data["descricao"],
        gravidade=data["gravidade"],
    )
    return jsonify({"msg": "Local cadastrado com sucesso!", "id": local_id}), 201

# Listagem de locais afetados
@app.route("/locais", methods=["GET"])
def listar_locais():
    return jsonify(list_locais()), 200

# Solicitação e oferta de ajuda (materiais, voluntários)
@app.route("/ajudas", methods=["POST"])
def registrar_ajuda():
    data = request.get_json() or {}
    required = ["tipo", "descricao", "contato"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

    ajuda_id = create_ajuda(
        tipo=data["tipo"],
        descricao=data["descricao"],
        contato=data["contato"],
        local_id=data.get("local_id"),
        status=data.get("status", "aberta"),
    )
    return jsonify({"msg": "Ajuda registrada com sucesso!", "id": ajuda_id}), 201

# Listagem de ajudas
@app.route("/ajudas", methods=["GET"])
def listar_ajudas():
    return jsonify(list_ajudas()), 200

# Listagem de bairros (catálogo interno)
@app.route("/bairros", methods=["GET"])
def listar_bairros():
    return jsonify(list_bairros()), 200

# Exibição de informações públicas (previsão do tempo) por coordenadas
# Exemplo: /publico/clima?lat=-25.43&lon=-52.71
@app.route("/publico/clima", methods=["GET"])
def publico_clima():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Parâmetros 'lat' e 'lon' são obrigatórios"}), 400

    ok, data = get_weather_by_coords(lat, lon)
    if ok:
        return jsonify(data), 200
    return jsonify({"error": "Não foi possível obter dados de clima", "detalhe": data}), 502

# Exibição de informações públicas (previsão do tempo) por bairro
# Exemplo: /publico/clima/bairro?bairro=Centro
@app.route("/publico/clima/bairro", methods=["GET"])
def publico_clima_bairro():
    bairro = request.args.get("bairro")
    if not bairro:
        return jsonify({"error": "Parâmetro 'bairro' é obrigatório"}), 400

    ok, data = get_weather_by_bairro(bairro)
    if ok:
        return jsonify(data), 200
    return jsonify({"error": "Não foi possível obter dados de clima para o bairro", "detalhe": data}), 404

if __name__ == "__main__":
    app.run(debug=True)
