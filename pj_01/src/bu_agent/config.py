"""Configuração central do agente."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path_value: str | None) -> Path:
    """Resolve caminhos relativos a partir da raiz do projeto."""
    if path_value is None:
        return ROOT / "data" / "bweb_2t_RN_261020260742.csv"

    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate

    project_candidate = ROOT / candidate
    return project_candidate if project_candidate.exists() else candidate


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("BU_MODEL", "qwen2.5:3b")
DATA_PATH = resolve_path(os.getenv("BU_DATA_PATH"))
MAX_STEPS = int(os.getenv("BU_MAX_STEPS", "5"))
