"""Bateria de testes das ferramentas — espelha os 11 testes do notebook."""
import pytest
from bu_agent.tools import (
    search_secoes, secao_details, compare_secoes,
    total_por_tipo, total_sem_biometria,
)


def test_search_nulos_presidente():
    r = search_secoes(cargo="Presidente", tipo_voto="Nulo", top_n=5)
    assert "error" not in r
    assert r["secoes"][0]["ZONA_N"] == 25
    assert r["secoes"][0]["SECAO_N"] == 105
    assert r["secoes"][0]["QT_VOTOS_N"] == 26


def test_search_nulos_governador():
    r = search_secoes(cargo="Governador", tipo_voto="Nulo", top_n=5)
    assert r["secoes"][0]["ZONA_N"] == 24
    assert r["secoes"][0]["SECAO_N"] == 35
    assert r["secoes"][0]["QT_VOTOS_N"] == 37


def test_search_sem_cargo():
    r = search_secoes(tipo_voto="Nulo", top_n=5)
    assert r["secoes"][0]["ZONA_N"] == 22
    assert r["secoes"][0]["SECAO_N"] == 41
    assert r["secoes"][0]["QT_VOTOS_N"] == 52


def test_tolerancia_cargo_com_tipo():
    """cargo='Nulo' deve ser movido para tipo_voto."""
    r = search_secoes(cargo="Nulo", tipo_voto="Nulo", top_n=5)
    assert "error" not in r
    assert r["secoes"][0]["QT_VOTOS_N"] == 52


def test_secao_details():
    r = secao_details(zona=3, secao=505)
    assert r["municipio"] == "NATAL"
    assert r["aptos"] == 460
    assert r["comparecimento"] == 432
    cargos = {v["DS_CARGO_PERGUNTA"] for v in r["votos"]}
    assert cargos == {"Governador", "Presidente"}


def test_compare_secoes():
    r = compare_secoes(zona_a=3, secao_a=505, zona_b=3, secao_b=504, tipo_voto="Nominal")
    assert "505" in r["resposta"]
    assert "838" in r["resposta"]
    assert "834" in r["resposta"]


def test_total_nominais():
    r = total_por_tipo(tipo_voto="Nominal")
    assert r["total_votos"] == 4264428


def test_total_brancos():
    r = total_por_tipo(tipo_voto="Branco")
    assert r["total_votos"] == 55812


def test_total_nulos():
    r = total_por_tipo(tipo_voto="Nulo")
    assert r["total_votos"] == 142093


def test_total_nulos_presidente():
    r = total_por_tipo(tipo_voto="Nulo", cargo="Presidente")
    assert r["cargo"] == "Presidente"
    assert r["total_votos"] > 0


def test_sem_biometria():
    r = total_sem_biometria()
    assert r["total_sem_biometria"] == 180838
    assert r["percentual"] == 6.8


def test_erro_cargo_invalido():
    r = search_secoes(cargo="Lula")
    assert "error" in r


def test_erro_secao_inexistente():
    r = secao_details(zona=999, secao=999)
    assert "error" in r