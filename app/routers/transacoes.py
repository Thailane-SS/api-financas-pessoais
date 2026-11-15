from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from app.database import SessaoDep
from app.models import (
    Categoria,
    Erro,
    Transacao,
    TransacaoAtualizar,
    TransacaoCriar,
    TransacaoLer,
)

router = APIRouter(prefix="/transacoes", tags=["Transações"])

ERRO_TRANSACAO = {404: {"model": Erro, "description": "Transação não encontrada"}}
ERRO_CATEGORIA = {404: {"model": Erro, "description": "Categoria não encontrada"}}
ERRO_AMBOS = {404: {"model": Erro, "description": "Transação ou categoria não encontrada"}}


def verificar_categoria(sessao: Session, categoria_id: int):
    if not sessao.get(Categoria, categoria_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada.",
        )


def buscar_transacao_ou_404(sessao: Session, transacao_id: int) -> Transacao:
    transacao = sessao.get(Transacao, transacao_id)
    if not transacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada.",
        )
    return transacao


@router.post(
    "",
    response_model=TransacaoLer,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar transação",
    responses=ERRO_CATEGORIA,
)
def criar_transacao(dados: TransacaoCriar, sessao: SessaoDep):
    verificar_categoria(sessao, dados.categoria_id)

    transacao = Transacao.model_validate(dados)
    sessao.add(transacao)
    sessao.commit()
    sessao.refresh(transacao)
    return transacao


@router.get("", response_model=list[TransacaoLer], summary="Listar transações")
def listar_transacoes(sessao: SessaoDep):
    consulta = select(Transacao).order_by(Transacao.data.desc(), Transacao.id.desc())
    return sessao.exec(consulta).all()


@router.get(
    "/{transacao_id}",
    response_model=TransacaoLer,
    summary="Buscar transação por id",
    responses=ERRO_TRANSACAO,
)
def buscar_transacao(transacao_id: int, sessao: SessaoDep):
    return buscar_transacao_ou_404(sessao, transacao_id)


@router.patch(
    "/{transacao_id}",
    response_model=TransacaoLer,
    summary="Editar transação",
    responses=ERRO_AMBOS,
)
def atualizar_transacao(transacao_id: int, dados: TransacaoAtualizar, sessao: SessaoDep):
    transacao = buscar_transacao_ou_404(sessao, transacao_id)

    alteracoes = dados.model_dump(exclude_unset=True, exclude_none=True)
    if "categoria_id" in alteracoes:
        verificar_categoria(sessao, alteracoes["categoria_id"])

    transacao.sqlmodel_update(alteracoes)
    sessao.add(transacao)
    sessao.commit()
    sessao.refresh(transacao)
    return transacao


@router.delete(
    "/{transacao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir transação",
    responses=ERRO_TRANSACAO,
)
def excluir_transacao(transacao_id: int, sessao: SessaoDep):
    transacao = buscar_transacao_ou_404(sessao, transacao_id)
    sessao.delete(transacao)
    sessao.commit()