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
chama funções Python que consultam o arquivo carregado.

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
- Jupyter, VS Code ou Google Colab;
- Ollama e um modelo local, por padrão `qwen2.5:3b`.

Os dados devem ser obtidos do CDN oficial:

```text
https://cdn.tse.jus.br/
```
