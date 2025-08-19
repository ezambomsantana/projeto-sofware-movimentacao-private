from app_service import validar_campos, calcular_valor, criar_objeto_movimentacao
from unittest.mock import patch, MagicMock

# ------------------------
# Testes do validar_campos
# ------------------------

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

def test_validar_campos_faltando():
    data = {
        "cpf_comprador": "123",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) == "Campo obrigatório 'cpf_vendedor' não informado"

# ------------------------
# Testes do calcular_valor
# ------------------------

@patch("app_service.requests.get")
def test_calcular_valor_ok(mock_get):
    # simula resposta da API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ticker": "PETR4", "preco": 37.50}
    mock_get.return_value = mock_response

    valor, erro = calcular_valor("PETR4", 10)

    assert valor == 375.0
    assert erro is None
    mock_get.assert_called_once_with("http://localhost:8080/stocks/PETR4", timeout=5)

@patch("app_service.requests.get")
def test_calcular_valor_ticker_nao_encontrado(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    valor, erro = calcular_valor("XYZ", 10)

    assert valor is None
    assert "Erro ao buscar ticker" in erro


# ------------------------
# Testes do criar_objeto_movimentacao
# ------------------------

def test_criar_objeto_movimentacao():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "VALE3",
        "quantidade": 2
    }
    valor_total = 124.6
    mov = criar_objeto_movimentacao(data, valor_total)
    assert mov["valor_movimentacao"] == valor_total
    assert mov["ticker"] == "VALE3"
