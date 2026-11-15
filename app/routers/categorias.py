from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.database import SessaoDep
from app.models import Categoria, CategoriaCriar, CategoriaLer, Erro

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post(
    "",
    response_model=CategoriaLer,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar categoria",
    responses={409: {"model": Erro, "description": "Já existe uma categoria com esse nome"}},
)
def criar_categoria(dados: CategoriaCriar, sessao: SessaoDep):
    existente = sessao.exec(
        select(Categoria).where(Categoria.nome == dados.nome)
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma categoria com esse nome.",
        )

    categoria = Categoria.model_validate(dados)
    sessao.add(categoria)
    sessao.commit()
    sessao.refresh(categoria)
    return categoria


@router.get("", response_model=list[CategoriaLer], summary="Listar categorias")
def listar_categorias(sessao: SessaoDep):
    return sessao.exec(select(Categoria).order_by(Categoria.nome)).all()


@router.get(
    "/{categoria_id}",
    response_model=CategoriaLer,
    summary="Buscar categoria por id",
    responses={404: {"model": Erro, "description": "Categoria não encontrada"}},
)
def buscar_categoria(categoria_id: int, sessao: SessaoDep):
    categoria = sessao.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada.",
        )
    return categoria