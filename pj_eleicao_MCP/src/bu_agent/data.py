"""Carregamento e normalização do BU."""
from pathlib import Path

import pandas as pd

from .config import DATA_PATH, resolve_path


def load_bu(path: str | Path | None = None) -> pd.DataFrame:
    """Carrega o BU enxuto e prepara as colunas derivadas."""
    data_path = resolve_path(str(path)) if path is not None else DATA_PATH
    if not data_path.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {data_path}")

    last_error = None
    for encoding in ("utf-8-sig", "latin1", "cp1252"):
        try:
            df = pd.read_csv(data_path, sep=";", encoding=encoding,
                             dtype=str, keep_default_na=False)
            break
        except UnicodeDecodeError as exc:
            last_error = exc
    else:
        raise last_error

    # padroniza os nomes que as funções esperam
    df = df.rename(columns={"NR_ZONA": "ZONA_N", "NR_SECAO": "SECAO_N"})

    # numéricas
    df["QT_VOTOS_N"] = pd.to_numeric(df["QT_VOTOS"], errors="coerce").fillna(0)
    df["ZONA_N"] = pd.to_numeric(df["ZONA_N"], errors="coerce")
    df["SECAO_N"] = pd.to_numeric(df["SECAO_N"], errors="coerce")

    # seção agregada (consolidada) — não tem seção única
    df["AGREGADA"] = df["DS_SECOES_AGREGADAS"] != "#NULO#"

    return df


def _parse_int(valor, nome):
    """Converte para int com mensagem de erro clara."""
    try:
        return int(valor), None
    except (TypeError, ValueError):
        return None, {"error": f"{nome} '{valor}' inválido. Use um número inteiro."}


def _num(v, default=0):
    """Converte para número com fallback seguro (NaN → default)."""
    n = pd.to_numeric(v, errors="coerce")
    return default if pd.isna(n) else n