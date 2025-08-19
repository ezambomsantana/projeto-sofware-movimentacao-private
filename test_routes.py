import pytest
from unittest.mock import patch
from app import app, movimentacoes

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_post_movimentacao_mock(client):
    movimentacoes.clear()
    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4",
        "quantidade": 10
    }

    # Mock das funções do app_service
    with patch("app.calcular_valor", return_value=(999.99, None)), \
         patch("app.criar_objeto_movimentacao") as mock_criar:

        mock_criar.side_effect = lambda data, valor: {
            "cpf_comprador": data["cpf_comprador"],
            "cpf_vendedor": data["cpf_vendedor"],
            "ticker": data["ticker"],
            "quantidade": data["quantidade"],
            "valor_movimentacao": valor
        }

        response = client.post("/movimentacoes", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["valor_movimentacao"] == 999.99
    assert data["ticker"] == "PETR4"

def test_get_movimentacoes(client):
    movimentacoes.clear()
    movimentacoes.append({
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "VALE3",
        "quantidade": 2,
        "valor_movimentacao": 124.6
    })

    response = client.get("/movimentacoes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["ticker"] == "VALE3"
