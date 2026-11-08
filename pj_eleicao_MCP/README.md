# Análise de Boletins de Urna (BUWeb)

Notebook para baixar e analisar os **Boletins de Urna (BUWeb)** oficiais do
Tribunal Superior Eleitoral (TSE). O projeto preserva o CSV original e usa
pandas para calcular os resultados consultados por um agente local do Ollama.

As consultas abrangem:

- votos de Governador e Presidente;
- votos nominais, brancos e nulos;
- zonas e seções eleitorais;
- aptos, comparecimento e abstenções;
- eleitores sem biometria válida;
- comparação entre duas seções.

O modelo não acessa a internet nem calcula resultados por conta própria. Ele
usa um host MCP que descobre as ferramentas publicadas pelo servidor
[`src/bu_agent/mcp_server.py`](./src/bu_agent/mcp_server.py), executado por
`stdio`, e consulta o arquivo carregado. Além das cinco ferramentas, o
servidor publica o resource `eleicao-RN://schema` e o prompt
`recomendar_analise`.

## Arquivos

- [pj_01.ipynb](./pj_01.ipynb): notebook principal;
- `planilhas/downloads/`: ZIPs baixados do TSE;
- `planilhas/*.csv`: CSV original extraído do ZIP.

## Como configurar a fonte do TSE

Na primeira célula, use **uma** das opções abaixo.

### Opção 1 — parâmetros e código de geração

```python
ANO = 2026
UF = "RN"
TURNO = 2
GERACAO_BU = "261020260742"
URL_BU = ""
```

O notebook monta o endereço no formato:

```text
https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{ANO}/buweb/bweb_{TURNO}t_{UF}_{GERACAO_BU}.zip
```

`GERACAO_BU` é o código exato que aparece no nome do ZIP. Ele pode mudar
conforme a UF, o turno ou uma atualização do arquivo; portanto, não é seguro
inferi-lo apenas com ano, UF e turno.

### Opção 2 — link completo

Quando o código não for conhecido, informe o endereço completo publicado pelo
TSE:

```python
URL_BU = (
    "https://cdn.tse.jus.br/estatistica/sead/eleicoes/"
    "eleicoes2026/buweb/bweb_2t_RN_261020260742.zip"
)
GERACAO_BU = ""
```

Quando preenchido, `URL_BU` tem prioridade. O notebook valida o domínio oficial
`cdn.tse.jus.br` e extrai do nome do arquivo o ano, a UF, o turno e a geração.
Para mudar do segundo para o primeiro turno, use um ZIP `bweb_1t_...` válido.

## Ordem e função das células

Execute as células em ordem.

### 1. Download do BUWeb oficial

Cria `planilhas/` e `planilhas/downloads/`, baixa o ZIP quando ele ainda não
existe, extrai o primeiro CSV encontrado e valida as colunas de Governador,
Presidente, tipos de voto, comparecimento, abstenções e biometria.

O arquivo usado pela análise é o CSV original extraído. Nenhuma coluna é
removida.

### 2. Confirmação e download do CSV original

Mostra o caminho e o tamanho do CSV. No Google Colab, também chama
`google.colab.files.download` para permitir que o usuário salve o arquivo no
computador.

### 3. Inspeção dos dados

Exibe o cabeçalho, o número de linhas, o número de colunas, os primeiros
registros e amostras de Governador e Presidente.

### 4. Preparação do Ollama

Confere a instalação do Ollama, tenta iniciar o servidor local quando necessário
e verifica se o modelo configurado está disponível.

### 5. Diagnóstico de GPU e velocidade

Verifica `nvidia-smi` antes de executá-lo, informa se há GPU NVIDIA e mede a
velocidade de geração. A análise continua em CPU quando não há GPU.

### 6. Utilitários

Define as funções auxiliares para chamar a API local do Ollama e exibir o
histórico da conversa.

### 7. Gabarito com pandas

Carrega o CSV original com `dtype=str`, preservando zeros à esquerda de zona,
seção e município. Renomeia os identificadores para `ZONA_N` e `SECAO_N` e
cria:

- `QT_VOTOS_N`: versão numérica de `QT_VOTOS`;
- `AGREGADA`: indica se a seção possui seções agregadas.

Essas colunas derivadas são necessárias pelas funções de análise.

### 8. Funções de análise

Implementa e registra em `FUNCTIONS`:

- `search_secoes`;
- `secao_details`;
- `compare_secoes`;
- `total_por_tipo`;
- `total_sem_biometria`.

As funções validam parâmetros, consultam o dataframe real e retornam erros
explícitos para filtros inválidos ou sem resultados.

### 9. Schemas das ferramentas

Define em `TOOLS` os nomes, descrições, tipos e parâmetros que o Ollama pode
usar para chamar cada função.

### 10. Prompt do agente e loop de execução

Define as regras de resposta em português, o escopo dos dados e a obrigação de
usar as ferramentas. Em seguida executa o fluxo:

1. envia a pergunta ao modelo;
2. recebe a chamada de ferramenta;
3. executa a função Python;
4. devolve o resultado ao modelo;
5. exibe a resposta final.

### 11. Bateria final

Executa perguntas de validação sobre totais, zonas, seções, comparação,
biometria e perguntas fora do escopo. O resultado mostra quantos testes foram
aprovados e reprovados.

### 12. Perguntas livres

Abre um loop para perguntas manuais sobre o arquivo carregado. Use `sair`,
`exit` ou `q` para encerrar.

## Execução no Google Colab

O caminho `Path.cwd()` normalmente corresponde a `/content`. Esse armazenamento
é temporário e pode ser apagado quando a sessão termina.

Para conservar os dados:

1. execute a célula de confirmação para baixar o CSV para o computador; ou
2. monte o Google Drive e execute o notebook em uma pasta persistente.

Se o ZIP já existir em `planilhas/downloads/`, a célula reutiliza o arquivo em
vez de baixá-lo novamente.

## Requisitos

- Python 3;
- pandas;
- requests;
- fastmcp 4.1.4;
- Jupyter, VS Code ou Google Colab;
- Ollama e um modelo local, por padrão `qwen2.5:7b`.

Instale as dependências com:

```bash
python -m pip install -r requirement.txt
```

Para inspecionar o servidor MCP sem iniciar o Ollama, use o cliente Python do
FastMCP ou o MCP Inspector apontando para
`src/bu_agent/mcp_server.py`. O agente de linha de comando pode ser iniciado
com:

```bash
PYTHONPATH=src python -m bu_agent.cli
```

### Executar o servidor MCP no VS Code

O servidor usa `stdio`, portanto o comando abaixo fica aguardando mensagens e
não deve ser encerrado por parecer travado:

```bash
PYTHONPATH=src .venv/bin/python src/bu_agent/mcp_server.py
```

Para registrar o servidor automaticamente no VS Code, abra a pasta do projeto
e use a configuração em [`.vscode/mcp.json`](./.vscode/mcp.json). Depois:

1. abra a paleta de comandos;
2. execute **MCP: List Servers**;
3. selecione `eleicao-rn`;
4. escolha **Start**.

Se o ambiente virtual ainda não existir, crie-o e instale as dependências:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirement.txt
```

## Sequência de teste

Execute os passos abaixo a partir da raiz do projeto. Eles validam primeiro os
dados e as funções, depois o servidor MCP e, por fim, o fluxo completo com o
Ollama.

### 1. Preparar o ambiente

```bash
cd "/mnt/ssd/projeto eleição/pj_eleicao_MCP"
python3 -m venv .venv                 # execute apenas se ainda não existir
.venv/bin/pip install -r requirement.txt
```

Confirme que o arquivo de dados está presente:

```bash
test -f data/bweb_2t_RN_261020260742.csv && echo "dados encontrados"
```

### 2. Executar os testes automatizados

```bash
.venv/bin/pytest -q
```

Resultado esperado:

```text
13 passed
```

### 3. Conferir o Ollama e o modelo

Em um terminal separado do servidor MCP, verifique o serviço e os modelos:

```bash
curl http://localhost:11434/api/version
ollama list
```

O modelo usado pelo projeto é definido por `BU_MODEL`. O padrão atual é
`qwen2.5:7b`. Para usar o modelo `qwen2.5:3b`, que também é compatível:

```bash
BU_MODEL=qwen2.5:3b
```

Se o Ollama não estiver em execução:

```bash
ollama serve
```

### 4. Testar o servidor MCP sem Ollama

Este comando inicia o servidor por `stdio` e verifica as ferramentas, o
resource e o prompt. Ele deve ser executado em um segundo terminal; o processo
do servidor fica ativo somente durante o teste:

```bash
PYTHONPATH=src .venv/bin/python - <<'PY'
import asyncio
from pathlib import Path
from fastmcp import Client

async def main():
    async with Client(Path("src/bu_agent/mcp_server.py")) as client:
        tools = await client.list_tools()
        print("ferramentas:", [tool.name for tool in tools])

        total = await client.call_tool(
            "total_por_tipo",
            {"tipo_voto": "Nulo", "cargo": "Presidente"},
        )
        print("total:", total.data)

        schema = await client.read_resource("eleicao-RN://schema")
        print("resource:", bool(schema))

        prompt = await client.get_prompt(
            "recomendar_analise",
            {"cargo": "Presidente", "tipo_voto": "Nulo"},
        )
        print("prompt:", bool(prompt.messages))

asyncio.run(main())
PY
```

Os valores esperados incluem:

```text
ferramentas: ['total_por_tipo', 'total_sem_biometria', 'secao_details', 'compare_secoes', 'search_secoes']
total: {'total_votos': 61879, ...}
resource: True
prompt: True
```

### 5. Executar o agente completo

Em outro terminal, inicie o agente:

```bash
PYTHONPATH=src .venv/bin/python -m bu_agent.cli
```

Faça estas perguntas, uma por vez:

```text
Quantos votos nulos para presidente existem?
Quais seções têm mais votos nulos para governador?
Me dê os detalhes da seção 505 da zona 3.
Compare os votos nominais da seção 505 com a 504 da zona 3.
Quantos eleitores estão sem biometria válida no total?
```

O terminal deve mostrar a sequência ReAct, com uma chamada MCP entre a
pergunta e a resposta final:

```text
── volta 1 ──
🤖 o modelo pediu → total_por_tipo(...)
🔧 nós executamos → ...
── volta 2 ──
🤖 o modelo respondeu com texto → fim do loop
```

Encerre com `sair`, `exit` ou `q`.

### 6. Diagnóstico rápido

- **`model ... not found`**: instale o modelo ou defina `BU_MODEL` para um nome
  exibido por `ollama list`.
- **`Connection refused`**: inicie o Ollama com `ollama serve`.
- **O servidor parece travado**: isso é esperado quando ele é iniciado
  diretamente; o transporte `stdio` fica aguardando um cliente MCP.
- **`13 passed`**: as funções eleitorais e os dados locais foram validados.

Os dados devem ser obtidos do CDN oficial:

```text
https://cdn.tse.jus.br/
```
