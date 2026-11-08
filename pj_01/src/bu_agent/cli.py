"""Interface de linha de comando."""
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
            run_agent(pergunta)
        except RuntimeError as exc:
            print(f"\n❌ {exc}\n")
            print("Dica: rode no terminal: ollama serve")
            print("Depois: ollama pull qwen2.5:3b\n")


if __name__ == "__main__":
    main()