# BU Eleições 2026 RN — Agente Auditor

Agente de auditoria em linguagem natural sobre o Boletim de Urna (BU) das Eleições 2026 do Rio Grande do Norte. Usa um loop ReAct com cinco ferramentas MCP e um modelo local via Ollama.

## Arquitetura MCP

[`src/bu_agent/mcp_server.py`](./src/bu_agent/mcp_server.py) é o servidor
FastMCP executado por `stdio`. Ele publica as cinco ferramentas de análise,
o resource `eleicao-RN://schema` com as colunas do BU e o prompt
`recomendar_analise`. O agente em [`src/bu_agent/agent.py`](./src/bu_agent/agent.py)
atua como host MCP: descobre as ferramentas com `list_tools` e executa cada
chamada com `call_tool`; as funções de análise permanecem em
[`src/bu_agent/tools.py`](./src/bu_agent/tools.py).

## O que faz

- "Quais seções têm mais votos nulos para presidente?"
- "Me dá os detalhes da seção 505 da zona 3."
- "Compara os votos nominais da seção 505 com a 504 da zona 3."
- "Qual o total de votos nominais no arquivo?"
- "Quantos eleitores estão sem biometria válida no total?"

## Ferramentas

| Ferramenta | Uso |
|---|---|
| `search_secoes` | Top N seções por votos, com filtros de tipo, cargo, zona |
| `secao_details` | Dados completos de uma seção |
| `compare_secoes` | Compara duas seções |
| `total_por_tipo` | Total de votos no arquivo |
| `total_sem_biometria` | Total de eleitores sem biometria |

## Instalação

```

Para inspecionar o servidor sem Ollama:

```bash
fastmcp list src/bu_agent/mcp_server.py --resources --prompts --input-schema
fastmcp call src/bu_agent/mcp_server.py total_por_tipo tipo_voto=Nulo cargo=Presidente
```

Para iniciar o agente:

```bash
PYTHONPATH=src python -m bu_agent.cli
```bash
git clone https://github.com/<seu-usuario>/bu-eleicoes-rn.git
cd bu-eleicoes-rn
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirement.txt