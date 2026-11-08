"""Host do agente: Ollama decide e o servidor MCP executa."""
import json
from pathlib import Path

import requests
from fastmcp import Client

from .config import MAX_STEPS, MODEL, OLLAMA_URL
from .prompts import SYSTEM
from .summary import summary


def ensure_ollama_available():
    """Valida se o serviço local do Ollama está disponível."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        models = r.json().get("models", [])
        available = [model.get("name") for model in models if model.get("name")]
        if MODEL not in available:
            nomes = ", ".join(available) or "nenhum modelo instalado"
            raise RuntimeError(
                f"O modelo '{MODEL}' não está instalado no Ollama. "
                f"Modelos disponíveis: {nomes}. "
                f"Defina BU_MODEL ou execute 'ollama pull {MODEL}'."
            )
    except RuntimeError:
        raise
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Ollama não está disponível em {OLLAMA_URL}. "
            "Inicie o serviço com 'ollama serve'."
        ) from exc
    except (ValueError, KeyError) as exc:
        raise RuntimeError(
            f"Ollama respondeu em {OLLAMA_URL}, mas retornou uma resposta "
            "inválida em /api/tags."
        ) from exc


def llm(messages, tools=None):
    """Uma chamada ao /api/chat do Ollama. Devolve o JSON inteiro."""
    ensure_ollama_available()
    body = {"model": MODEL, "messages": messages, "stream": False,
            "options": {"temperature": 0, "num_predict": 600}}
    if tools:
        body["tools"] = tools
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=body, timeout=300)
        r.raise_for_status()
    except requests.HTTPError as exc:
        detalhe = r.text.strip()
        raise RuntimeError(
            f"Ollama rejeitou a chamada a /api/chat (HTTP {r.status_code}). "
            f"{detalhe}"
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Falha ao chamar o Ollama em {OLLAMA_URL}/api/chat."
        ) from exc
    return r.json()


def _to_ollama(tool):
    """Converte a descrição de uma ferramenta MCP para o formato do Ollama."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        },
    }


async def run_agent(pedido, max_steps=MAX_STEPS, verbose=True):
    """Executa o loop ReAct através do servidor MCP."""
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": pedido}]
    if verbose:
        print(f"👤 {pedido}\n")

    async with Client(Path(__file__).with_name("mcp_server.py")) as client:
        tools = [_to_ollama(tool) for tool in await client.list_tools()]

        for volta in range(1, max_steps + 1):
            if verbose:
                print(f"── volta {volta} " + "─" * 60)

            msg = llm(messages, tools=tools)["message"]
            messages.append(msg)

            if not msg.get("tool_calls"):
                if verbose:
                    print("🤖 o modelo respondeu com texto → fim do loop\n")
                    print(msg["content"])
                return messages

            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                raw = call["function"].get("arguments", {})
                args = raw if isinstance(raw, dict) else json.loads(raw or "{}")

                if verbose:
                    print(
                        f"🤖 o modelo pediu     → {name}"
                        f"({json.dumps(args, ensure_ascii=False)})"
                    )

                result = await client.call_tool(
                    name, args, raise_on_error=False
                )
                if result.is_error:
                    content = result.content[0].text
                    if verbose:
                        print(f"📡 o servidor        → erro: {content}")
                else:
                    content = result.content[0].text
                    if verbose:
                        print(f"🔧 nós executamos    → {summary(result.data)}")

                messages.append(
                    {"role": "tool", "tool_name": name, "content": content}
                )

    if verbose:
        print(f"(parei depois de {max_steps} voltas sem resposta final)")
    return messages