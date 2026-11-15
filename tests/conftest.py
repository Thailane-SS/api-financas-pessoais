import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import obter_sessao
from app.main import app


@pytest.fixture
def client():
    # Banco SQLite em memória: novo e vazio a cada teste
    engine_teste = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine_teste)

    def obter_sessao_teste():
        with Session(engine_teste) as sessao:
            yield sessao

    app.dependency_overrides[obter_sessao] = obter_sessao_teste
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def categorias(client):
    """Cadastra categorias de exemplo e devolve um dicionário nome -> id."""
    ids = {}
    for nome in ["Alimentação", "Transporte", "Salário"]:
        resposta = client.post("/categorias", json={"nome": nome})
        ids[nome] = resposta.json()["id"]
    return ids