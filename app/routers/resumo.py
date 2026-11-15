from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import func, select

from app.database import SessaoDep
from app.models import (
    Categoria,
    GastoPorCategoria,
    ResumoMensal,
    TipoTransacao,
    Transacao,
)

router = APIRouter(prefix="/resumo", tags=["Resumo"])


def periodo_do_mes(ano: int, mes: int) -> tuple[date, date]:
    inicio = date(ano, mes, 1)
    if mes == 12:
        fim = date(ano + 1, 1, 1)
    else:
        fim = date(ano, mes + 1, 1)
    return inicio, fim


@router.get("", response_model=ResumoMensal, summary="Resumo financeiro do mês")
def resumo_mensal(
    sessao: SessaoDep,
    ano: Annotated[int, Query(ge=2000, le=2100, description="Ano, ex.: 2026")],
    mes: Annotated[int, Query(ge=1, le=12, description="Mês de 1 a 12")],
):
    inicio, fim = periodo_do_mes(ano, mes)
    no_periodo = (Transacao.data >= inicio, Transacao.data < fim)

    # Total por tipo (receita / despesa): SUM + GROUP BY
    consulta_totais = (
        select(Transacao.tipo, func.sum(Transacao.valor))
        .where(*no_periodo)
        .group_by(Transacao.tipo)
    )
    totais = {tipo: total for tipo, total in sessao.exec(consulta_totais).all()}

    total_receitas = totais.get(TipoTransacao.receita) or Decimal("0.00")
    total_despesas = totais.get(TipoTransacao.despesa) or Decimal("0.00")

    # Despesas por categoria: JOIN + SUM + GROUP BY
    soma = func.sum(Transacao.valor)
    consulta_categorias = (
        select(Categoria.id, Categoria.nome, soma)
        .join(Categoria, Transacao.categoria_id == Categoria.id)
        .where(*no_periodo, Transacao.tipo == TipoTransacao.despesa)
        .group_by(Categoria.id, Categoria.nome)
        .order_by(soma.desc())
    )
    por_categoria = [
        GastoPorCategoria(categoria_id=cat_id, categoria=nome, total=total)
        for cat_id, nome, total in sessao.exec(consulta_categorias).all()
    ]

    return ResumoMensal(
        ano=ano,
        mes=mes,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=total_receitas - total_despesas,
        despesas_por_categoria=por_categoria,
    )