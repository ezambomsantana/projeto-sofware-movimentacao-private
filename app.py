from flask import Flask, request, jsonify
from app_service import validar_campos, calcular_valor, criar_objeto_movimentacao

app = Flask(__name__)

# "Banco de dados" em memória
movimentacoes = []

# ------------------------
# Rotas
# ------------------------

@app.route("/movimentacoes", methods=["POST"])
def criar_movimentacao():
    data = request.get_json()

    erro = validar_campos(data)
    if erro:
        return jsonify({"erro": erro}), 400

    valor_total, erro = calcular_valor(data["ticker"], data["quantidade"])
    if erro:
        return jsonify({"erro": erro}), 400

    movimentacao = criar_objeto_movimentacao(data, valor_total)

    movimentacoes.append(movimentacao)
    return jsonify(movimentacao), 201


@app.route("/movimentacoes", methods=["GET"])
def listar_movimentacoes():
    return jsonify(movimentacoes)


if __name__ == "__main__":
    app.run(debug=True)
