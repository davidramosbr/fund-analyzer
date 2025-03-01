import subprocess
from bs4 import BeautifulSoup
import requests

def buscar_noticias(nome_fundo):
    termo_pesquisa = f"{nome_fundo} fundo imobiliário"
    url = f"https://news.google.com/search?q={termo_pesquisa}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar o Google News.")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    noticias = []
    for artigo in soup.find_all("article"):
        titulo = artigo.find("a", class_="JtKRv").get_text()
        link = artigo.find("a", class_="JtKRv")["href"]
        link = f"https://news.google.com{link}"
        noticias.append({"titulo": titulo, "link": link})
    return noticias

def avaliar_noticia(titulo):
    prompt = (
        "Avalie o título da notícia abaixo e atribua uma nota de 0 a 100, onde:\n"
        "- 0: Notícia extremamente negativa/pessimista para o fundo.\n"
        "- 50: Notícia neutra/irrelevante para o fundo.\n"
        "- 100: Notícia extremamente positiva/otimista para o fundo.\n"
        "Por favor, retorne APENAS UM NÚMERO INTEIRO entre 0 e 100, sem texto adicional.\n\n"
        "Exemplos:\n"
        "- Título: 'Fundo XYZ tem queda recorde em seu valor de mercado'\n"
        "  Nota: 10\n"
        "- Título: 'Fundo XYZ anuncia aumento de 20% nos dividendos'\n"
        "  Nota: 95\n"
        "- Título: 'Fundo XYZ mantém estabilidade em relatório trimestral'\n"
        "  Nota: 50\n\n"
        "Agora, avalie este título:\n"
        f"'{titulo}'\n"
        "Nota:"
    )
    comando = ["ollama", "run", "qwen2.5:3b", prompt]
    resultado = subprocess.run(comando, capture_output=True, text=True, encoding='latin1')
    try:
        nota = int(resultado.stdout.strip().encode('latin1').decode('utf-8', errors='ignore'))
        return max(0, min(100, nota))
    except ValueError:
        print(f"Erro ao processar a nota para o título: {titulo}")
        return 50
    
def avaliar_noticias(noticias):
    notas = [avaliar_noticia(noticia["titulo"]) for noticia in noticias]
    nota_global = sum(notas) / len(notas) if notas else 50
    return notas, nota_global
