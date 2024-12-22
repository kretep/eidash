import os
import requests
from datetime import datetime

class BirthdayData:

    def __init__(self):
        self.birthdays = []

    def get_data(self):
        try:
            self.birthdays = self.fetch_data()
        except Exception as e:
            print(e)
        return self.birthdays

    def fetch_data(self):
        url = os.environ["HKDASH_BIRTHDAY_URL"]

        # Current date
        now = datetime.now()
        params = {
            "month": f"eq.{now.month}",
            "day": f"eq.{now.day}"
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Check and parse the response
        if response.status_code == 200:
            result = response.json()  # List of dictionaries representing the rows
        else:
            print(f"Error: {response.status_code}, {response.text}")

        return result
