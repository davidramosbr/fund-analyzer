import json

def validar_fundo(nome_fundo):
    try:
        with open("data/fundos_setores.json", "r") as f:
            fundos = json.load(f)
    except FileNotFoundError:
        print("Arquivo fundos_setores.json não encontrado.")
        return False
    except json.JSONDecodeError:
        print("Erro ao ler fundos_setores.json.")
        return False

    return nome_fundo.upper() in fundos
