"""Formata o resultado de cada ferramenta em texto pt-BR."""


def summary(result):
    if not isinstance(result, dict):
        return str(result)

    if "error" in result:
        return f'❌ erro: {result["error"]}'

    if "total_found" in result:
        secoes = [f'{s["ZONA_N"]}/{s["SECAO_N"]} ({s["NM_MUNICIPIO"]}): {s["QT_VOTOS_N"]}'
                  for s in result.get("secoes", [])]
        return f'{result["total_found"]} seções. Top: ' + " | ".join(secoes)

    if "total_sem_biometria" in result:
        pct = result.get("percentual")
        pct_txt = f" ({str(pct).replace('.', ',')}% dos aptos)" if pct is not None else ""
        total = f'{result["total_sem_biometria"]:,}'.replace(",", ".")
        return f'{total} sem biometria{pct_txt} em {result["secoes"]} seções'

    if "total_votos" in result and "secoes" not in result:
        filtro = result.get("tipo_voto") or "todos os tipos"
        cargo = result.get("cargo")
        if cargo:
            filtro = f"{filtro} para {cargo}"
        linhas = result.get("linhas")
        total = f'{result["total_votos"]:,}'.replace(",", ".")
        base = f'{total} votos ({filtro})'
        return f'{base} em {linhas} linhas' if linhas is not None else base

    if "resposta" in result:
        return result["resposta"]

    if "votos" in result:
        por_cargo = {}
        for v in result["votos"]:
            por_cargo.setdefault(v["DS_CARGO_PERGUNTA"], 0)
            por_cargo[v["DS_CARGO_PERGUNTA"]] += v["QT_VOTOS"]
        totais = " | ".join(f'{k}: {v}' for k, v in por_cargo.items())
        return (f'Seção {result["zona"]}/{result["secao"]} — {result["municipio"]}: '
                f'{result["aptos"]} aptos, {result["comparecimento"]} comparecimento. '
                f'Votos por cargo: {totais}')

    return str(result)[:300]