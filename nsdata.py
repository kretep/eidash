#!/usr/bin/python
# -*- coding: <encoding name> -*-
 
from datetime import datetime
import requests
import os

class NightscoutException(Exception): pass

class NSData:

    def __init__(self):
        self.entries = []

    def get_entries(self, retries=0, last_exception=None):
        if retries >= 3:
            print("Retried too many times: %s" % last_exception)
            raise NightscoutException(last_exception)

        try:
            host = os.environ['NSDASH_URL']
            resp = requests.get(f'{host}/api/v1/entries/sgv.json?count=2', verify=False, timeout=5)
                # For the sake of keeping this portable without adding a lot of complexity, don't verify SSL certificates.
                # https://github.com/kennethreitz/requests/issues/557
                # Don't let bad connectivity cause the app to freeze
        except requests.exceptions.Timeout as e:
            # Don't retry timeouts, since the app is unresponsive while a request is in progress,
            # and a new request will be made in UPDATE_FREQUENCY_SECONDS seconds anyway.
            print("Timed out: %s" % repr(e))
            raise NightscoutException(repr(e))
        except requests.exceptions.RequestException as e:
            return self.get_entries(retries + 1, repr(e))

        if resp.status_code != 200:
            return self.get_entries(retries + 1, "Nightscout returned status %s" % resp.status_code)

        try:
            arr = resp.json()
            if type(arr) == list and (len(arr) == 0 or type(arr[0]) == dict):
                return arr
            else:
                return self.get_entries(retries + 1, "Nightscout returned bad data")
        except simplejson.scanner.JSONDecodeError:
            return self.get_entries(retries + 1, "Nightscout returned bad JSON")

    def maybe_convert_units(self, mgdl):
        #TODO: make  config/env var
        return round(mgdl / 18.0182, 1) if True else mgdl

    def filter_bgs(self, entries):
        bgs = [e.copy() for e in entries if 'sgv' in e]
        for bg in bgs:
            bg['sgv'] = int(bg['sgv'])
        return bgs

    def minutes_ago(self, timestamp):
        return int((datetime.timestamp(datetime.now()) - timestamp / 1000) / 60)

    def get_direction(self, entry):
        return {
            'DoubleUp': u'⇈',
            'SingleUp': u'↑',
            'FortyFiveUp': u'↗',
            'Flat': u'→',
            'FortyFiveDown': u'↘',
            'SingleDown': u'↓',
            'DoubleDown': u'⇊',
        }.get(entry.get('direction'), '-')

    def get_delta(self, last, second_to_last):
        if (last['date'] - second_to_last['date']) / 1000 > 1000:
            return '?'
        return ('+' if last['sgv'] >= second_to_last['sgv'] else u'−') + \
            str(abs(self.maybe_convert_units(last['sgv'] - second_to_last['sgv'])))

    def get_data(self):
        minutes_ago = -1
        bgs = self.filter_bgs(self.entries)
        if len(bgs) > 1:
            last, second_to_last = bgs[0:2]
            minutes_ago = self.minutes_ago(last['date'])

        # Check whether it is useful to get new data
        if minutes_ago >= 5 or minutes_ago < 0:
            self.entries = entries = self.get_entries()
            bgs = self.filter_bgs(entries)
            last, second_to_last = bgs[0:2]
            minutes_ago = self.minutes_ago(last['date'])

        return {
            "sgv": self.maybe_convert_units(last['sgv']),
            "direction": self.get_direction(last),
            "minutes_ago": minutes_ago,
            "delta": self.get_delta(last, second_to_last)
        }
