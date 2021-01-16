from datetime import datetime, timedelta
import os
import requests

class SunspotNumber:

    def __init__(self):
        self.data = {}
        self.last_refetch_time = None

    def get_data(self):
        if self.needs_refetch():
            try:
                raw_data = self.refetch()
                if raw_data is not None:
                    self.data = self.process_data(raw_data)
                    self.last_refetch_time = datetime.now()
            except Exception as e:
                print(e)
        return self.data
    
    def refetch(self):
        try:
            url = os.getenv("EIDASH_SUNSPOT_NUMBER_URL")
            response = requests.get(url)
            return response.text
        except Exception as e:
            print(e)

    def process_data(self, data):
        return {
            "sunspot_number": data.split('\n')[-2].split(',')[4].strip()
        }

    def needs_refetch(self):
        if self.last_refetch_time is None:
            return True
        elapsed = datetime.now() - self.last_refetch_time
        return elapsed >= timedelta(minutes=360)
