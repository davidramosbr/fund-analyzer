import requests
from bs4 import BeautifulSoup

class Scrapping:
    def __init__(self):
        self.base_url = 'https://www.fundsexplorer.com.br/funds/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def get_url(self, fund_code):
        return f'{self.base_url}{fund_code}'

    def fetch_page(self, fund_code):
        url = self.get_url(fund_code)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_fund_data(self, fund_code):
        # Retorna o HTML bruto da página
        raw_data = self.fetch_page(fund_code)
        if raw_data is None:
            return {}
        return raw_data
