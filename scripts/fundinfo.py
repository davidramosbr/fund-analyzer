from scripts.scrapping import Scrapping
from scripts.processing import Processing
import os
import json

class FundInfo:
    def __init__(self):
        self.scrapping = Scrapping() 
        self.processing = None

    def get_fund_data(self, fund_code):
        raw_data = self.scrapping.get_fund_data(fund_code)

        if raw_data:
            self.processing = Processing(raw_data)
            processed_data = self.processing.process_data()
            return processed_data
        else:
            file_path = f"processing/{fund_code}.json"
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    processed_data = json.load(file)
                return processed_data
            else:
                return {}

    def get_fund_data_local_first(self, fund_code):
        file_path = f"processing/{fund_code}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                processed_data = json.load(file)
            return processed_data
        else:
            raw_data = self.scrapping.get_fund_data(fund_code)
            if raw_data:
                self.processing = Processing(raw_data)
                processed_data = self.processing.process_data()
                return processed_data
            else:
                return {}
