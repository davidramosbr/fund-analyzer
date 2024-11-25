from bs4 import BeautifulSoup
from scripts.functions import Functions
import os
import json

class Processing:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.soup = BeautifulSoup(self.raw_data, 'html.parser')

    def process_data(self):
        fund_name = self.soup.find("h1", class_="headerTicker__content__title").text.strip() if self.soup.find("h1", class_="headerTicker__content__title") else "Nome não encontrado"
        fund_setor = self.soup.find("section", {"id": "carbon_fields_fiis_comparator_simulator-2"}).find_all("span")[2].find('i').text.strip()
        ul_comparator = self.soup.find("ul", class_="comparator__cols__list comparator__cols__list--data")
        patrimonio_liquido = Functions.convert_to_int(ul_comparator.find("li", {"data-row": "patrimonioLiquido"}).text.strip()) if ul_comparator.find("li", {"data-row": "patrimonioLiquido"}) else 0
        fund_price = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "cotacao"}).text.strip()) if ul_comparator.find("li", {"data-row": "cotacao"}) else 0.0
        value_per_share = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "vpCota"}).text.strip()) if ul_comparator.find("li", {"data-row": "vpCota"}) else 0.0
        pvp = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "pvp"}).text.strip()) if ul_comparator.find("li", {"data-row": "pvp"}) else 0.0
        liquidez_media_diaria = Functions.convert_to_int(ul_comparator.find("li", {"data-row": "liquidezMediaDiaria"}).text.strip()) if ul_comparator.find("li", {"data-row": "liquidezMediaDiaria"}) else 0.0
        cotistas = Functions.convert_to_int(ul_comparator.find("li", {"data-row": "cotistas"}).text.strip()) if ul_comparator.find("li", {"data-row": "cotistas"}) else 0
        ultimo_rendimento = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "ultimoRendimento"}).text.strip()) if ul_comparator.find("li", {"data-row": "ultimoRendimento"}) else 0.0
        yield_mensal = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "yieldMensal"}).text.strip()) if ul_comparator.find("li", {"data-row": "yieldMensal"}) else 0.0
        yield_anual = Functions.convert_to_float(ul_comparator.find("li", {"data-row": "yieldAnual"}).text.strip()) if ul_comparator.find("li", {"data-row": "yieldAnual"}) else 0.0

        fund_data = {
            "fund_name": fund_name,
            "patrimonio_liquido": patrimonio_liquido,
            "fund_price": fund_price,
            "value_per_share": value_per_share,
            "pvp": pvp,
            "liquidez_media_diaria": liquidez_media_diaria,
            "cotistas": cotistas,
            "ultimo_rendimento": ultimo_rendimento,
            "yield_mensal": yield_mensal,
            "yield_anual": yield_anual,
            "setor": fund_setor,
        }
        self.save_data_json(fund_name, fund_data)
        return fund_data

    def save_data_json(self, fund_name, data_array):
        if not os.path.exists('processing'):
            os.makedirs('processing')
        file_path = os.path.join('processing', f'{fund_name}.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data_array, file, ensure_ascii=False, indent=4)