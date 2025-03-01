import json

def classificar_setor(nome_fundo):
    with open("data/fundos_setores.json", "r") as f:
        fundos = json.load(f)
    return fundos.get(nome_fundo.upper(), "outros")
