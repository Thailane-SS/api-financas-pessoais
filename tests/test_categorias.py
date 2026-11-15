def test_criar_categoria(client):
    resposta = client.post("/categorias", json={"nome": "Lazer"})

    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["nome"] == "Lazer"
    assert "id" in dados


def test_criar_categoria_remove_espacos(client):
    resposta = client.post("/categorias", json={"nome": "  Lazer  "})

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Lazer"


def test_nao_permite_categoria_duplicada(client):
    client.post("/categorias", json={"nome": "Lazer"})
    resposta = client.post("/categorias", json={"nome": "Lazer"})

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "Já existe uma categoria com esse nome."


def test_nao_permite_nome_vazio(client):
    resposta = client.post("/categorias", json={"nome": "   "})

    assert resposta.status_code == 422


def test_listar_categorias_em_ordem_alfabetica(client, categorias):
    resposta = client.get("/categorias")

    assert resposta.status_code == 200
    nomes = [categoria["nome"] for categoria in resposta.json()]
    assert nomes == ["Alimentação", "Salário", "Transporte"]


def test_buscar_categoria_inexistente(client):
    resposta = client.get("/categorias/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Categoria não encontrada."