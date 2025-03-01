from modules.validation import validar_fundo
from modules.news_manager import buscar_noticias, avaliar_noticias
from modules.setor_classifier import classificar_setor
from modules.data_manager import buscar_historico, calcular_nota_complexa, salvar_dados, calcular_nota_relacao, calcular_nota_rendimento
from modules.avaliator import salvar_informacao, avaliacao_final

def capturar_nome_fundo():
    print("Você pode inserir somente o nome do fundo ou varios nomes separados apenas por virgula.")
    entrada = input("Digite o nome do fundo imobiliário: ").strip()
    if "," in entrada:
        fundos = entrada.split(",")
        fundos = [fundo.strip().upper() for fundo in fundos]
        return fundos
    else:
        return entrada.upper()

def iniciar_processos(nome_fundo):
    print(f"Iniciando análise para o fundo: {nome_fundo}")
    salvar_informacao(f"Iniciando análise para o fundo: {nome_fundo}")

    if validar_fundo(nome_fundo):
        print(f"O fundo {nome_fundo} é válido. Prosseguindo com a análise...")
        print("Buscando notícias recentes...")
        noticias = buscar_noticias(nome_fundo)
        if noticias:
            print(f"Notícias encontradas para {nome_fundo}:")
            salvar_informacao(f"Notícias encontradas para {nome_fundo}:")
            notas, nota_global = avaliar_noticias(noticias)
            for noticia, nota in zip(noticias, notas):
                print(f"Notícia: {noticia['titulo']}\nNota: {nota}")
                salvar_informacao(f"Notícia: {noticia['titulo']}\nNota: {nota}")
            print(f"Nota de notícias para {nome_fundo}: {nota_global:.2f}")
            salvar_informacao(f"Nota de notícias para {nome_fundo}: {nota_global:.2f}")
        else:
            print("Nenhuma notícia recente encontrada.")
        print("Buscando histórico de preços e dividendos...")
        historico = buscar_historico(nome_fundo)
        setor = classificar_setor(nome_fundo)
        print(f"Setor do fundo: {setor}")
        salvar_informacao(f"Setor do fundo: {setor}")
        salvar_dados(nome_fundo, setor, historico)
        nota_final = calcular_nota_complexa(historico, noticias)
        avaliacao = avaliacao_final(nome_fundo, setor)
        print(f"A nota final é: {nota_final}\nAvaliação: {avaliacao}")
        salvar_informacao(f"A nota final é: {nota_final}\nAvaliação: {avaliacao}")
    else:
        print(f"O fundo {nome_fundo} não foi encontrado ou é inválido.")

if __name__ == "__main__":
    nome_fundo = capturar_nome_fundo()
    if isinstance(nome_fundo, list):
        for nome in nome_fundo:
            iniciar_processos(nome)
    else:
        iniciar_processos(nome_fundo)