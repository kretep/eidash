import os
import requests

class WeatherData:

    def __init__(self):
        pass

    def get_data(self):
        try:
            wl_key = os.environ['HKDASH_WL_KEY']
            wl_location = os.environ['HKDASH_WL_LOCATION']
            resp = requests.get(f'http://weerlive.nl/api/json-data-10min.php?key={wl_key}&locatie={wl_location}', verify=False, timeout=5)
        except requests.exceptions.Timeout as e:
            # Don't retry timeouts, since the app is unresponsive while a request is in progress,
            # and a new request will be made in UPDATE_FREQUENCY_SECONDS seconds anyway.
            print("Timed out: %s" % repr(e))
            raise Exception(repr(e))
        except requests.exceptions.RequestException as e:
            return {}
        if resp.status_code != 200:
            return {}

        try:
            data = resp.json()
            if type(data) == dict:
                return data['liveweer'][0]
            else:
                return {}
        except simplejson.scanner.JSONDecodeError:
            return {}
