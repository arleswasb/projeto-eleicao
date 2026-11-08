# Projeto Eleição

Repositório principal que reúne os projetos relacionados à análise de dados
eleitorais e ao uso de agentes de IA.

## Estrutura

### [`pj_01/`](./pj_01/)

Projeto de análise dos Boletins de Urna (BUWeb) oficiais do Tribunal Superior
Eleitoral (TSE). O projeto inclui notebook, dados de apoio, funções Python para
consultas e testes.

Consulte o [README do pj_01](./pj_01/README.md) para obter:

- instruções de download dos dados do TSE;
- configuração e execução do notebook;
- integração com o Ollama;
- descrição das funções de análise;
- requisitos do projeto.

### [`pj_eleicao_MCP/`](./pj_eleicao_MCP/)

Projeto relacionado ao uso de MCP (Model Context Protocol) com os dados e
funcionalidades eleitorais.

Consulte o [README do pj_eleicao_MCP](./pj_eleicao_MCP/README.md) para obter as
instruções específicas de instalação, configuração e execução.

## Requisitos gerais

Os requisitos podem variar entre os projetos. Cada pasta possui seu próprio
arquivo `requirement.txt`; instale as dependências no ambiente virtual
correspondente ao projeto que será executado.

Exemplo:

```bash
cd pj_01
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirement.txt
```

No Windows PowerShell, ative o ambiente com:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Dados eleitorais

Os dados do BUWeb devem ser obtidos do CDN oficial do TSE:

<https://cdn.tse.jus.br/>

Arquivos baixados e dados gerados localmente não devem ser incluídos no
repositório quando estiverem cobertos pelo `.gitignore`.

## Desenvolvimento

Para executar os testes de um dos projetos, entre na respectiva pasta e use o
comando definido na documentação local. Quando aplicável, o comando padrão é:

```bash
python -m pytest
```

## Organização do Git

Este diretório é o repositório Git principal. `pj_01` e `pj_eleicao_MCP` são
pastas de projeto dentro dele, e não devem conter diretórios `.git` ativos.
