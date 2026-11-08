"""Servidor MCP das ferramentas de auditoria eleitoral."""

import sys
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP

if __package__:
    from . import tools
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from bu_agent import tools

TipoVoto = Literal["Nulo", "Branco", "Nominal"]
Cargo = Literal["Governador", "Presidente"]

mcp = FastMCP("eleicao-RN")


@mcp.tool
def total_por_tipo(
    tipo_voto: TipoVoto | None = None,
    cargo: Cargo | None = None,
) -> dict:
    """Total de votos por tipo, opcionalmente filtrado por cargo."""
    return tools.total_por_tipo(tipo_voto=tipo_voto, cargo=cargo)


@mcp.tool
def total_sem_biometria(
    zona: int | None = None,
    municipio: str | None = None,
) -> dict:
    """Total de eleitores sem biometria válida no arquivo inteiro.

    Para o total geral, chame sem argumentos.
    """
    return tools.total_sem_biometria(zona=zona, municipio=municipio)


@mcp.tool
def secao_details(zona: int, secao: int) -> dict:
    """Todos os dados de uma seção."""
    return tools.secao_details(zona=zona, secao=secao)


@mcp.tool
def compare_secoes(
    zona_a: int,
    secao_a: int,
    zona_b: int,
    secao_b: int,
    tipo_voto: TipoVoto | None = None,
) -> dict:
    """Compara duas seções lado a lado, agregando por cargo."""
    return tools.compare_secoes(
        zona_a=zona_a,
        secao_a=secao_a,
        zona_b=zona_b,
        secao_b=secao_b,
        tipo_voto=tipo_voto,
    )


@mcp.tool
def search_secoes(
    tipo_voto: TipoVoto | None = None,
    zona: int | None = None,
    cargo: Cargo | None = None,
    min_votos: int | None = None,
    top_n: int = 5,
) -> dict:
    """Busca seções no BU por tipo de voto, zona, cargo e mínimo de votos."""
    return tools.search_secoes(
        tipo_voto=tipo_voto,
        zona=zona,
        cargo=cargo,
        min_votos=min_votos,
        top_n=top_n,
    )


@mcp.resource("eleicao-RN://schema")
def schema() -> str:
    """As colunas do Boletim de Urna."""
    return ", ".join(tools.bu.columns)


@mcp.prompt
def recomendar_analise(
    cargo: Cargo,
    tipo_voto: TipoVoto,
    top_n: int = 5,
) -> str:
    """Pede uma análise de seções com cargo e tipo de voto preenchidos."""
    return (
        f"Analise as seções com mais votos {tipo_voto} para {cargo}. "
        f"Use a ferramenta search_secoes com cargo='{cargo}', "
        f"tipo_voto='{tipo_voto}' e top_n={top_n}. "
        f"Liste as {top_n} primeiras citando zona, seção, município e o total "
        "de votos. Depois aponte a seção com o maior valor e o quanto ela "
        "supera a segunda colocada."
    )


if __name__ == "__main__":
    mcp.run()