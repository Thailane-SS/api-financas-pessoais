from datetime import date
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel


class TipoTransacao(str, Enum):
    receita = "receita"
    despesa = "despesa"


class CategoriaBase(SQLModel):
    nome: str = Field(index=True, unique=True, max_length=50)


class Categoria(CategoriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CategoriaCriar(CategoriaBase):
    pass


class CategoriaLer(CategoriaBase):
    id: int


class TransacaoBase(SQLModel):
    descricao: str = Field(max_length=200)
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    tipo: TipoTransacao
    data: date
    categoria_id: int = Field(foreign_key="categoria.id")


class Transacao(TransacaoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TransacaoCriar(TransacaoBase):
    pass


class TransacaoLer(TransacaoBase):
    id: int


class TransacaoAtualizar(SQLModel):
    descricao: str | None = None
    valor: Decimal | None = None
    tipo: TipoTransacao | None = None
    data: date | None = None
    categoria_id: int | None = None