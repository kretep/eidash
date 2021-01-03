
from datetime import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import os

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
        transport = RequestsHTTPTransport(url=os.environ["HKDASH_BIRTHDAY_URL"])
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        query MyQuery ($month: Int!, $day: Int!) {
            birthdays (where: {month:{_eq: $month}, day:{_eq: $day}})
            {
                name
                year
                month
                day
            }
        }
        """)
        now = datetime.now()
        params = {
            "month": now.month,
            "day": now.day
        }

        result = client.execute(query, variable_values=params)
        return result["birthdays"]
