from scripts.fundinfo import FundInfo
from scripts.calculate import calculate_fund_scores
from time import sleep as wait

wallet = {
    'YEES11': 0,
    'XPML11': 0,
    'XPLG11': 0,
    'XPIN11': 0,
    'XPCI11': 0,
    'VLIQ11': 0,
    'VISC11': 0,
    'VGRI11': 0,
    'VGHF11': 0,
    'VCRI11': 0,
    'SPTW11': 0,
    'SNFF11': 0,
    'SNAG11': 0,
    'SADI11': 0,
    'RZAG11': 0,
    'RECR11': 0,
    'RBRF11': 0,
    'QAGR11': 0,
    'PORD11': 0,
    'PMFO11': 0,
    'PCAS11': 0,
    'NSLU11': 0,
    'NCRA11': 0,
    'MXRF11': 0,
    'MCCI11': 0,
    'LVBI11': 0,
    'KNSC11': 0,
    'KNRI11': 0,
    'KNIP11': 0,
    'KDIF11': 0,
    'JRDM11': 0,
    'JPPA11': 0,
    'JCDB11': 0,
    'ITIT11': 0,
    'IRDM11': 0,
    'HSML11': 0,
    'HLMB11': 0,
    'HGLG11': 0,
    'HCRI11': 0,
    'GVBI11': 0,
    'DAMA11': 0,
    'COPP11': 0,
    'BZLI11': 0,
    'BODB11': 0,
    'BARI11': 0,
    'AZPL11': 0,
    'AURB11': 0,
}

def clean_wallet():
    global wallet
    wallet = {fund: quantity for fund, quantity in wallet.items() if quantity > 0}

def print_wallet(wallet):
    print("Estado atual da carteira:")
    sortedwallet = sorted(wallet.items(), key=lambda x: x[1], reverse=True)
    for fund, quantity in sortedwallet:
        print(f"{fund}: {quantity} unidades")
    print("-" * 30)

def main():
    for i in range(1000):

        print_wallet(wallet)


        fund_data = []
        fund_info = FundInfo()
        for fund_code, value in wallet.items():
            data = fund_info.get_fund_data_local_first(fund_code)
            if data:
                fund_data.append([
                    fund_code,
                    data['fund_price'],
                    data['patrimonio_liquido'],
                    data['pvp'],
                    data['liquidez_media_diaria'],
                    data['cotistas'],
                    data['ultimo_rendimento'],
                    data['yield_mensal'], 
                    data['yield_anual'],
                    value,
                    data['setor']
                ])
        
        fund_scores = calculate_fund_scores(fund_data)
        sorted_funds = sorted(zip(wallet.keys(), fund_scores), key=lambda x: x[1], reverse=True)
        fundname, score = sorted_funds[0]
        
        print(f"O fundo recomendado é {fundname}.")
        response = "s"

        if (i > 100):
            clean_wallet()

        if response.lower() == "s":
            wallet[fundname] += 1
            print(f"Você comprou uma unidade do fundo {fundname}. Novo valor na carteira: {wallet[fundname]}")
        elif response.lower() == "n":
            print("Nenhuma alteração feita. Encerrando o programa.")
        else:
            print("Resposta inválida. Encerrando o programa.")


if __name__ == "__main__":
    main()
