"""Schemas das ferramentas no formato de function calling do Ollama."""

TOOLS = [
    {"type": "function",
     "function": {
         "name": "search_secoes",
         "description": ("Busca seções no Boletim de Urna por tipo de voto "
                         "(Nulo, Branco, Nominal), zona eleitoral, cargo "
                         "(Governador ou Presidente) e mínimo de votos. "
                         "Devolve quantas seções bateram no filtro e as 5 com "
                         "mais votos."),
         "parameters": {
             "type": "object",
             "properties": {
                 "tipo_voto": {
                     "type": "string",
                     "enum": ["Nulo", "Branco", "Nominal"],
                     "description": ("Tipo de voto a filtrar. OMITA para buscar "
                                     "todos os tipos.")
                 },
                 "zona": {
                     "type": "integer",
                     "description": ("Número da zona eleitoral. OMITA para buscar "
                                     "em todas as zonas. NÃO passe 0.")
                 },
                 "cargo": {
                     "type": "string",
                     "enum": ["Governador", "Presidente"],
                     "description": ("Cargo a filtrar. NÃO use 'Nulo', 'Branco' "
                                     "ou 'Nominal' aqui. OMITA para todos os cargos.")
                 },
                 "min_votos": {
                     "type": "integer",
                     "description": "Mínimo de votos na seção"
                 },
                 "top_n": {
                     "type": "integer",
                     "description": "Quantas seções devolver (padrão 5)"
                 },
             },
             "required": [],
         }}},

    {"type": "function",
     "function": {
         "name": "total_sem_biometria",
         "description": ("Total de eleitores sem biometria válida no arquivo, "
                         "opcionalmente filtrado por zona ou município. "
                         "Devolve também o percentual sobre os aptos. "
                         "Aceita APENAS zona e municipio — NÃO aceita tipo_voto, "
                         "cargo, min_votos nem top_n."),
         "parameters": {
             "type": "object",
             "properties": {
                 "zona": {
                     "type": "integer",
                     "description": "Número da zona. OMITA para todas as zonas."
                 },
                 "municipio": {
                     "type": "string",
                     "description": "Nome do município. OMITA para todos."
                 },
             },
             "required": [],
         }}},

    {"type": "function",
     "function": {
         "name": "secao_details",
         "description": ("Todos os dados de uma seção: aptos, comparecimento, "
                         "abstenções, horários, eleitores sem biometria, e os "
                         "votos agregados por cargo e tipo de voto."),
         "parameters": {
             "type": "object",
             "properties": {
                 "zona": {"type": "integer", "description": "Número da zona"},
                 "secao": {"type": "integer", "description": "Número da seção"},
             },
             "required": ["zona", "secao"],
         }}},

    {"type": "function",
     "function": {
         "name": "compare_secoes",
         "description": ("Compara duas seções lado a lado (aptos, "
                         "comparecimento, abstenções, votos por cargo). "
                         "Devolve o total de votos de cada seção e o vencedor "
                         "de cada critério."),
         "parameters": {
             "type": "object",
             "properties": {
                 "zona_a": {"type": "integer"},
                 "secao_a": {"type": "integer"},
                 "zona_b": {"type": "integer"},
                 "secao_b": {"type": "integer"},
                 "tipo_voto": {
                     "type": "string",
                     "enum": ["Nulo", "Branco", "Nominal"],
                     "description": ("Tipo de voto a comparar. OMITA para somar "
                                     "todos os tipos.")
                 },
             },
             "required": ["zona_a", "secao_a", "zona_b", "secao_b"],
         }}},

    {"type": "function",
     "function": {
         "name": "total_por_tipo",
         "description": ("Total de votos no arquivo inteiro, opcionalmente "
                         "filtrado por tipo de voto e/ou cargo. Use quando o "
                         "usuário pedir um total geral, não uma lista de seções."),
         "parameters": {
             "type": "object",
             "properties": {
                 "tipo_voto": {
                     "type": "string",
                     "enum": ["Nulo", "Branco", "Nominal"],
                     "description": "OMITA para somar todos os tipos de voto."
                 },
                 "cargo": {
                     "type": "string",
                     "enum": ["Governador", "Presidente"],
                     "description": "OMITA para somar os dois cargos."
                 },
             },
             "required": [],
         }}},
]