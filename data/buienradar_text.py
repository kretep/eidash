
from datetime import datetime, timedelta
import os
import requests

class BuienradarText:

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
            lat = os.getenv("EIDASH_LATITUDE")
            lon = os.getenv("EIDASH_LONGITUDE")
            if lat is None or lon is None:
                return ''
            url = f'https://gpsgadget.buienradar.nl/data/raintext?lat={lat}&lon={lon}'
            response = requests.get(url)
            return response.text
        except Exception as e:
            print(e)

    def process_data(self, data):
        # Split lines, filter empty values
        lines = list(filter(None, data.split('\n')))
        tuples = [(line.split('|')[1].strip(), line.split('|')[0].strip()) for line in lines]
        return tuples

    def needs_refetch(self):
        if self.last_refetch_time is None:
            return True
        elapsed = datetime.now() - self.last_refetch_time
        return elapsed >= timedelta(minutes=10)
