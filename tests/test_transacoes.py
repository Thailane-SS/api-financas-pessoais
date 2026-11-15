import pytest


def nova_transacao(categoria_id, **alteracoes):
    """Monta um JSON de transação válido; dá para trocar campos com alteracoes."""
    dados = {
        "descricao": "Mercado do mês",
        "valor": 350.90,
        "tipo": "despesa",
        "data": "2026-11-10",
        "categoria_id": categoria_id,
    }
    dados.update(alteracoes)
    return dados


def test_criar_transacao(client, categorias):
    resposta = client.post("/transacoes", json=nova_transacao(categorias["Alimentação"]))

    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["descricao"] == "Mercado do mês"
    assert dados["valor"] == "350.90"
    assert dados["tipo"] == "despesa"


def test_criar_transacao_com_categoria_inexistente(client):
    resposta = client.post("/transacoes", json=nova_transacao(999))

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Categoria não encontrada."


@pytest.mark.parametrize(
    "campo, valor_invalido",
    [
        ("valor", 0),
        ("valor", -50),
        ("valor", 10.999),
        ("descricao", "   "),
        ("tipo", "gasto"),
        ("data", "2026-13-40"),
    ],
)
def test_recusa_dados_invalidos(client, categorias, campo, valor_invalido):
    dados = nova_transacao(categorias["Alimentação"], **{campo: valor_invalido})
    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_listar_transacoes_da_mais_recente_para_a_mais_antiga(client, categorias):
    id_alimentacao = categorias["Alimentação"]
    client.post("/transacoes", json=nova_transacao(id_alimentacao, descricao="Dia 5", data="2026-11-05"))
    client.post("/transacoes", json=nova_transacao(id_alimentacao, descricao="Dia 12", data="2026-11-12"))
    client.post("/transacoes", json=nova_transacao(id_alimentacao, descricao="Dia 10", data="2026-11-10"))

    resposta = client.get("/transacoes")

    assert resposta.status_code == 200
    descricoes = [transacao["descricao"] for transacao in resposta.json()]
    assert descricoes == ["Dia 12", "Dia 10", "Dia 5"]


def test_buscar_transacao_inexistente(client):
    resposta = client.get("/transacoes/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Transação não encontrada."


def test_editar_apenas_o_valor(client, categorias):
    criada = client.post("/transacoes", json=nova_transacao(categorias["Alimentação"])).json()

    resposta = client.patch(f"/transacoes/{criada['id']}", json={"valor": 399.50})

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["valor"] == "399.50"
    assert dados["descricao"] == criada["descricao"]
    assert dados["data"] == criada["data"]


def test_editar_com_valor_negativo(client, categorias):
    criada = client.post("/transacoes", json=nova_transacao(categorias["Alimentação"])).json()

    resposta = client.patch(f"/transacoes/{criada['id']}", json={"valor": -1})

    assert resposta.status_code == 422


def test_editar_com_categoria_inexistente(client, categorias):
    criada = client.post("/transacoes", json=nova_transacao(categorias["Alimentação"])).json()

    resposta = client.patch(f"/transacoes/{criada['id']}", json={"categoria_id": 999})

    assert resposta.status_code == 404


def test_excluir_transacao(client, categorias):
    criada = client.post("/transacoes", json=nova_transacao(categorias["Alimentação"])).json()

    resposta = client.delete(f"/transacoes/{criada['id']}")
    assert resposta.status_code == 204

    resposta = client.get(f"/transacoes/{criada['id']}")
    assert resposta.status_code == 404