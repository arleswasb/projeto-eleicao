"""Loop ReAct do agente."""
import json

import requests

from .config import MAX_STEPS, MODEL, OLLAMA_URL
from .prompts import SYSTEM
from .summary import summary
from .tools import FUNCTIONS, TOOLS


def ensure_ollama_available():
    """Valida se o serviço local do Ollama está disponível."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            "Ollama não está disponível em localhost:11434. "
            "Inicie o serviço com 'ollama serve' e confirme o modelo com 'ollama pull qwen2.5:3b'."
        ) from exc


def llm(messages, tools=None):
    """Uma chamada ao /api/chat do Ollama. Devolve o JSON inteiro."""
    ensure_ollama_available()
    body = {"model": MODEL, "messages": messages, "stream": False,
            "options": {"temperature": 0, "num_predict": 600}}
    if tools:
        body["tools"] = tools
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=body, timeout=300)
    r.raise_for_status()
    return r.json()


def run_agent(pedido, max_steps=MAX_STEPS, verbose=True):
    """Executa o loop ReAct e devolve o histórico de mensagens."""
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": pedido}]
    if verbose:
        print(f"👤 {pedido}\n")

    for volta in range(1, max_steps + 1):
        if verbose:
            print(f"── volta {volta} " + "─" * 60)

        msg = llm(messages, tools=TOOLS)["message"]
        messages.append(msg)

        if not msg.get("tool_calls"):
            if verbose:
                print("🤖 o modelo respondeu com texto → fim do loop\n")
                print(msg["content"])
            return messages

        for c in msg["tool_calls"]:
            name = c["function"]["name"]
            raw = c["function"]["arguments"]
            args = raw if isinstance(raw, dict) else json.loads(raw or "{}")

            if verbose:
                print(f"🤖 o modelo pediu     → {name}({json.dumps(args, ensure_ascii=False)})")

            try:
                result = FUNCTIONS[name](**args)
            except Exception as e:
                result = {"error": f"{type(e).__name__}: {e}"}

            if verbose:
                print(f"🔧 nós executamos    → {summary(result)}")

            messages.append({"role": "tool", "tool_name": name,
                             "content": json.dumps(result, ensure_ascii=False)})

    if verbose:
        print(f"(parei depois de {max_steps} voltas sem resposta final)")
    return messages