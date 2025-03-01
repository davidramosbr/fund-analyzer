import yfinance as yf
import json
import os
from modules.news_manager import avaliar_noticias 

def buscar_historico(nome_fundo):
    ticker = f"{nome_fundo}.SA"
    fundo = yf.Ticker(ticker)
    try:
        historico = fundo.history(period="1y", interval="1mo")
        if historico.empty:
            print(f"Nenhum dado encontrado para {nome_fundo}.")
            return []
        dados_formatados = []
        for data, row in historico.iterrows():
            preco = round(row["Close"], 2)
            dividendo = round(row["Dividends"], 2)
            relacao = round(dividendo / preco, 4) if preco > 0 else 0
            dados_formatados.append({
                "data": data.strftime("%Y-%m-%d"),
                "preco": preco,
                "dividendo": dividendo,
                "relacao_preco_dividendo": relacao
            })
        return dados_formatados
    except Exception as e:
        print(f"Erro ao buscar dados de {nome_fundo}: {e}")
        return []

def salvar_dados(nome_fundo, setor, dados):
    pasta_setor = os.path.join("data", setor)
    os.makedirs(pasta_setor, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_setor, f"{nome_fundo}.json")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump({"dados_meses": dados}, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {caminho_arquivo}")

def calcular_nota_relacao(dados, nome_fundo):
    if not dados or len(dados) < 2:
        return 50
    relacoes = [d["relacao_preco_dividendo"] for d in dados]
    inicio = relacoes[0]
    fim = relacoes[-1]
    variacao_total = abs((fim - inicio) / inicio) * 100 if inicio > 0 else 0
    print(f"Variação total: {variacao_total}")
    if variacao_total <= 5:
        nota = 100
    elif variacao_total <= 10:
        nota = 100 - (variacao_total - 5) * 10
    elif variacao_total <= 25:
        nota = 50 - (variacao_total - 10) * 2
    else:
        nota = 0
    variacoes = [(relacoes[i] - relacoes[i - 1]) for i in range(1, len(relacoes))]
    positivos = sum(1 for v in variacoes if v > 0)
    negativos = sum(1 for v in variacoes if v < 0)
    if positivos > negativos:
        nota = min(nota + (nota * 0.1), 100)
    caminho_arquivo = os.path.join("output", "reports", "notas_relacao.json")
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            notas_relacao = json.load(f)
    else:
        notas_relacao = {}
    notas_relacao[nome_fundo] = nota
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(notas_relacao, f, indent=4, ensure_ascii=False)
    print(f"Nota relação do fundo {nome_fundo} salva como {nota}.")
    return nota

def calcular_nota_rendimento(nome_fundo, dados):
    if not dados:
        return 0
    total = len(dados)
    nota = sum(d["relacao_preco_dividendo"] * 1000 for d in dados) / total
    nota = max(0, min(200, (nota - 7) * (200 / (12 - 7))))
    caminho_arquivo = os.path.join("output", "reports", "notas_rendimento.json")
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            notas_rendimento = json.load(f)
    else:
        notas_rendimento = {}
    notas_rendimento[nome_fundo] = nota
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(notas_rendimento, f, indent=4, ensure_ascii=False)
    print(f"Nota rendimento do fundo {nome_fundo} salva como {nota}.")
    return nota

def calcular_nota_complexa(historico, noticias):
    score_normalization = {
        'rendimento': 100,
        'estabilidade': 100,
        'noticias': 100
    }
    if not historico or len(historico) < 2:
        return 50
    relacoes = [d["relacao_preco_dividendo"] for d in historico]
    media_relacao = sum(relacoes) / len(relacoes)
    rendimento_score = (score_normalization['rendimento'] / 2) + (score_normalization['rendimento'] / 2) * media_relacao
    precos = [d["preco"] for d in historico]
    variacao_preco = (precos[-1] - precos[0]) / precos[0] if precos[0] > 0 else 0
    estabilidade_score = (score_normalization['estabilidade'] / 2) + (score_normalization['estabilidade'] / 2) * (1 - abs(variacao_preco))
    if noticias:
        _, nota_global = avaliar_noticias(noticias)
    else:
        nota_global = 50
    noticias_score = (score_normalization['noticias'] / 2) + (score_normalization['noticias'] / 2) * (nota_global / 100)
    nota_final = (rendimento_score + estabilidade_score + noticias_score) / 3
    return nota_final