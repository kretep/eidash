#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import locale
import logging

from data.nightscout import NightscoutData
from data.weather import WeatherData
from data.ephem import EphemData
from data.birthdays import BirthdayData
from data.sunspot_image import SunspotImage
from data.sunspot_number import SunspotNumber
from data.buienradar_text import BuienradarText
from data.kp_index import KpIndexData

from draw.hkdraw import HKDraw
from esp32_client import send_image
# from pixel.nightscout_pixel import draw_ns_pixel, turn_off_pixel

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.ERROR)
logging.error(f"##### Application start at {datetime.now()} ######")

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

    logging.info("Starting")
    width = 800
    height = 480

    logging.info("Init")

    # Initialize data sources
    dataSources = {
        "nightscout": NightscoutData(),
        "weather": WeatherData(),
        "ephem": EphemData(),
        "birthdays": BirthdayData(),
        "sunspot_image": SunspotImage(),
        "sunspot_number": SunspotNumber(),
        "buienradar_text": BuienradarText(),
        "kp_index": KpIndexData()
    }

    # Initialize drawing target
    hkdraw = HKDraw(width, height)

    isStandby = False

    while True:
        # Check if we should sleep
        now = datetime.now()
        if now.hour <= 6:
            if not isStandby:
                hkdraw.clear_image()
                send_image(hkdraw.context.image)
                #turn_off_pixel()
                isStandby = True
        else:
            isStandby = False

        if not isStandby:
            # Retrieve data
            data = {}
            for key, source in dataSources.items():
                logging.info("GET DATA for " + key)
                try:
                    data[key] = source.get_data()
                except Exception as err:
                    data[key] = { "error": str(err) }

            # Save the data (for debugging)
            # with open('debug_data.json', 'w') as outfile:
            #     json.dump(data, outfile)

            # Draw
            hkdraw.draw_data(data)

            # Pixel
            # if not "error" in data["nightscout"]:
            #     draw_ns_pixel(data["nightscout"])

            # Display
            send_image(hkdraw.context.image)

        # Sleep until the next update
        now = datetime.now()
        minutes_to_go = 4 - now.minute % 5
        seconds_to_go = 60 - now.second + minutes_to_go * 60
        logging.info(f"Sleeping for {seconds_to_go} seconds")
        time.sleep(seconds_to_go)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
