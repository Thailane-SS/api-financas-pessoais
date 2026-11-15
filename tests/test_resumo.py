def cadastrar(client, descricao, valor, tipo, data, categoria_id):
    resposta = client.post(
        "/transacoes",
        json={
            "descricao": descricao,
            "valor": valor,
            "tipo": tipo,
            "data": data,
            "categoria_id": categoria_id,
        },
    )
    assert resposta.status_code == 201


def test_resumo_do_mes(client, categorias):
    cadastrar(client, "Salário", 4500.00, "receita", "2026-11-05", categorias["Salário"])
    cadastrar(client, "Mercado", 350.90, "despesa", "2026-11-10", categorias["Alimentação"])
    cadastrar(client, "Uber", 30.00, "despesa", "2026-11-12", categorias["Transporte"])

    resposta = client.get("/resumo", params={"ano": 2026, "mes": 11})

    assert resposta.status_code == 200
    resumo = resposta.json()
    assert resumo["total_receitas"] == "4500.00"
    assert resumo["total_despesas"] == "380.90"
    assert resumo["saldo"] == "4119.10"
    assert resumo["despesas_por_categoria"] == [
        {"categoria_id": categorias["Alimentação"], "categoria": "Alimentação", "total": "350.90"},
        {"categoria_id": categorias["Transporte"], "categoria": "Transporte", "total": "30.00"},
    ]


def test_resumo_de_mes_sem_transacoes(client):
    resposta = client.get("/resumo", params={"ano": 2026, "mes": 10})

    assert resposta.status_code == 200
    resumo = resposta.json()
    assert resumo["total_receitas"] == "0.00"
    assert resumo["total_despesas"] == "0.00"
    assert resumo["saldo"] == "0.00"
    assert resumo["despesas_por_categoria"] == []


def test_resumo_considera_apenas_o_mes_pedido(client, categorias):
    id_alimentacao = categorias["Alimentação"]
    cadastrar(client, "Último dia de novembro", 10.00, "despesa", "2026-11-30", id_alimentacao)
    cadastrar(client, "Dezembro", 20.00, "despesa", "2026-12-15", id_alimentacao)
    cadastrar(client, "Primeiro dia de janeiro", 40.00, "despesa", "2027-01-01", id_alimentacao)

    resposta = client.get("/resumo", params={"ano": 2026, "mes": 12})

    assert resposta.json()["total_despesas"] == "20.00"


def test_resumo_soma_centavos_sem_erro_de_arredondamento(client, categorias):
    id_alimentacao = categorias["Alimentação"]
    cadastrar(client, "Bala", 0.10, "despesa", "2026-11-01", id_alimentacao)
    cadastrar(client, "Chiclete", 0.20, "despesa", "2026-11-02", id_alimentacao)

    resposta = client.get("/resumo", params={"ano": 2026, "mes": 11})

    assert resposta.json()["total_despesas"] == "0.30"


def test_resumo_com_mes_invalido(client):
    resposta = client.get("/resumo", params={"ano": 2026, "mes": 13})

    assert resposta.status_code == 422


def test_resumo_sem_informar_o_mes(client):
    resposta = client.get("/resumo", params={"ano": 2026})

    assert resposta.status_code == 422