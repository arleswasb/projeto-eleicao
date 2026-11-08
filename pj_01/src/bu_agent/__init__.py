"""Pacote BUWeb para análise de boletins de urna."""

__all__ = [
    "run_agent",
    "FUNCTIONS",
    "summary",
    "search_secoes",
    "secao_details",
    "compare_secoes",
    "total_por_tipo",
    "total_sem_biometria",
]


def __getattr__(name):
    if name == "run_agent":
        from .agent import run_agent
        return run_agent
    if name == "FUNCTIONS":
        from .tools import FUNCTIONS
        return FUNCTIONS
    if name == "summary":
        from .summary import summary
        return summary
    if name in {"search_secoes", "secao_details", "compare_secoes", "total_por_tipo", "total_sem_biometria"}:
        from .tools import (
            compare_secoes,
            search_secoes,
            secao_details,
            total_por_tipo,
            total_sem_biometria,
        )
        return {
            "search_secoes": search_secoes,
            "secao_details": secao_details,
            "compare_secoes": compare_secoes,
            "total_por_tipo": total_por_tipo,
            "total_sem_biometria": total_sem_biometria,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
