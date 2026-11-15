from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import criar_banco_e_tabelas
from app.routers import categorias


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_banco_e_tabelas()
    yield


app = FastAPI(
    title="API de Finanças Pessoais",
    description="API para registrar receitas e despesas e consultar resumos mensais.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(categorias.router)


@app.get("/")
def raiz():
    return {"mensagem": "API de Finanças Pessoais funcionando!"}


@app.get("/saude")
def saude():
    return {"status": "ok"}