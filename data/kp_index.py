from datetime import datetime
import requests

class KpIndexData:

    def __init__(self):
        self.api_endpoint = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"

    def get_data_from_api(self):
        return requests.get(self.api_endpoint, timeout=5).json()

    def get_data(self):
        data = self.get_data_from_api()
        return {
            "kp": data[-1][1]
        }
