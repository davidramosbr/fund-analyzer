from scripts.fundinfo import FundInfo
from scripts.neural import calculate_fund_scores

def main():

    # aqui vai ser quais fundos o usuário quer ter na carteira
    # posteriormente tenho que converter de forma que seja key => value (sendo value a quantidade de fundos na carteira)
    # dessa forma eu vou conseguir auxiliar na diversificação da wallet 
    
    fund_codes = [
        "XPML11", "VCRI11", "SNAG11", "MXRF11", "RBRF11"
    ]

    fund_data = []
    fund_info = FundInfo()
    for fund_code in fund_codes:
        data = fund_info.get_fund_data(fund_code)
        if (data != {}):
            fund_data.append([
                fund_code,
                data['fund_price'],
                data['patrimonio_liquido'],
                data['pvp'],
                data['liquidez_media_diaria'],
                data['cotistas'],
                data['ultimo_rendimento'],
                data['yield_mensal'], 
                data['yield_anual'] 
            ])
    
    fund_scores = calculate_fund_scores(fund_data)
    print("Pontuação dos Fundos (ordem decrescente):")
    sorted_funds = sorted(zip(fund_codes, fund_scores), key=lambda x: x[1], reverse=True)

    for code, score in sorted_funds:
        print(f"{code}: {int(score)}")


if __name__ == "__main__":
    main()
