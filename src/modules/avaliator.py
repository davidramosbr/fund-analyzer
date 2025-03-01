from datetime import datetime
import json
import os
import subprocess

todas_info = ''

def salvar_informacao(info):
    global todas_info
    todas_info += '\n'
    todas_info += info

def avaliacao_final(nome_fundo, setor):
    global todas_info
    prompt = (
        f"'{todas_info}'\n"
        "Considerando todas as informações que passei anteriormente, e as notas, qual sua avaliação final sobre esse fundo? é bom ou ruim? vale a pena ou não o investimento? seja conciso em sua avaliação e responda diretamente as questões, seja especifico com as respostas. Se necessário elabore mais a resposta. Liste também pontos chaves que considerou para essa avaliação."
    )
    comando = ["ollama", "run", "qwen2.5:7b", prompt]
    avaliacao = subprocess.run(comando, capture_output=True, text=True, encoding='latin1')
    resultado = avaliacao.stdout.strip()
    try:
        resultado = resultado.encode('latin1').decode('utf-8')
    except UnicodeDecodeError:
        try:
            resultado = resultado.encode('latin1').decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            pass
    salvar_dados(nome_fundo, setor, resultado)
    return resultado

def salvar_dados(nome_fundo, setor, resultado):
    pasta_results = os.path.join("output", "results", setor)
    os.makedirs(pasta_results, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_results, f"{nome_fundo}.json")
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump({"data": data_atual, "avaliacao": resultado}, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {caminho_arquivo}")