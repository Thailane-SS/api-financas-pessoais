def test_raiz_responde(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "API de Finanças Pessoais funcionando!"}


def test_saude_responde_ok(client):
    resposta = client.get("/saude")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}