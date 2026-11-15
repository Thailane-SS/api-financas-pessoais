from datetime import date
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel


class TipoTransacao(str, Enum):
    receita = "receita"
    despesa = "despesa"


class Erro(SQLModel):
    detail: str


# ---------- Categorias ----------

class CategoriaBase(SQLModel):
    nome: str = Field(index=True, unique=True, min_length=1, max_length=50)


class Categoria(CategoriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CategoriaCriar(CategoriaBase):
    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {"examples": [{"nome": "Lazer"}]},
    }


class CategoriaLer(CategoriaBase):
    id: int


# ---------- Transações ----------

class TransacaoBase(SQLModel):
    descricao: str = Field(min_length=1, max_length=200)
    valor: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    tipo: TipoTransacao
    data: date
    categoria_id: int = Field(foreign_key="categoria.id")


class Transacao(TransacaoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TransacaoCriar(TransacaoBase):
    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "examples": [
                {
                    "descricao": "Cinema com amigos",
                    "valor": 45.00,
                    "tipo": "despesa",
                    "data": "2026-11-14",
                    "categoria_id": 1,
                }
            ]
        },
    }


class TransacaoLer(TransacaoBase):
    id: int


class TransacaoAtualizar(SQLModel):
    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {"examples": [{"valor": 50.00}]},
    }

    descricao: str | None = Field(default=None, min_length=1, max_length=200)
    valor: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    tipo: TipoTransacao | None = None
    data: date | None = None
    categoria_id: int | None = None
    # ---------- Resumo mensal ----------

class GastoPorCategoria(SQLModel):
    categoria_id: int
    categoria: str
    total: Decimal


class ResumoMensal(SQLModel):
    ano: int
    mes: int
    total_receitas: Decimal
    total_despesas: Decimal
    saldo: Decimal
    despesas_por_categoria: list[GastoPorCategoria]