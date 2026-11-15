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


class Transacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao: str = Field(max_length=200)
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    tipo: TipoTransacao
    data: date
    categoria_id: int = Field(foreign_key="categoria.id")