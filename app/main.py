from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import criar_banco_e_tabelas
from app.routers import categorias, transacoes


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_banco_e_tabelas()
    yield


DESCRICAO_TAGS = [
    {"name": "Categorias", "description": "Grupos usados para organizar as transações (ex.: Alimentação, Transporte)."},
    {"name": "Transações", "description": "Receitas e despesas registradas."},
    {"name": "Status", "description": "Verificação de funcionamento da API."},
]

app = FastAPI(
    title="API de Finanças Pessoais",
    description="API para registrar receitas e despesas e consultar resumos mensais.",
    version="0.2.0",
    lifespan=lifespan,
    openapi_tags=DESCRICAO_TAGS,
)

app.include_router(categorias.router)
app.include_router(transacoes.router)


@app.get("/", tags=["Status"], summary="Mensagem de boas-vindas")
def raiz():
    return {"mensagem": "API de Finanças Pessoais funcionando!"}


@app.get("/saude", tags=["Status"], summary="Verificar se a API está no ar")
def saude():
    return {"status": "ok"}