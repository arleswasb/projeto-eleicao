# BU Eleições 2026 RN — Agente Auditor

Agente de auditoria em linguagem natural sobre o Boletim de Urna (BU) das Eleições 2026 do Rio Grande do Norte. Usa um loop ReAct com cinco ferramentas e um modelo local via Ollama.

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

```bash
git clone https://github.com/<seu-usuario>/bu-eleicoes-rn.git
cd bu-eleicoes-rn
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt