"""Interface de linha de comando."""
import asyncio

from .agent import run_agent


def main():
    print("Digite 'sair' para encerrar.\n")
    while True:
        try:
            pergunta = input("👤 ")
        except EOFError:
            print("\nEncerrando.")
            break
        if pergunta.strip().lower() in ("sair", "exit", "q"):
            break
        if not pergunta.strip():
            continue
        try:
            asyncio.run(run_agent(pergunta))
        except RuntimeError as exc:
            print(f"\n❌ {exc}\n")
            print("Dica: rode no terminal: ollama serve")
            print("Depois, instale ou escolha um modelo com BU_MODEL, por exemplo:")
            print("BU_MODEL=qwen2.5:7b PYTHONPATH=src .venv/bin/python -m bu_agent.cli\n")


if __name__ == "__main__":
    main()