#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import locale

import logging
from lib.waveshare_epd import epd7in5_V2
import json

from data.nightscout import NightscoutData
from data.weather import WeatherData
from data.ephem import EphemData
from data.birthdays import BirthdayData
from data.sunspot_image import SunspotImage
from data.sunspot_number import SunspotNumber
from data.buienradar_text import BuienradarText

from draw.hkdraw import HKDraw
from pixel.nightscout_pixel import draw_ns_pixel, turn_off_pixel

logging.basicConfig(level=logging.DEBUG)

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

    logging.info("Starting")
    epd = epd7in5_V2.EPD()
    width = epd.width # 800
    height = epd.height # 480

    logging.info("Init")
    epd.init()

    # Initialize data sources
    dataSources = {
        "nightscout": NightscoutData(),
        "weather": WeatherData(),
        "ephem": EphemData(),
        "birthdays": BirthdayData(),
        "sunspot_image": SunspotImage(),
        "sunspot_number": SunspotNumber(),
        "buienradar_text": BuienradarText()
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
                epd.display(epd.getbuffer(hkdraw.context.image))
                turn_off_pixel()
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
            if not "error" in data["nightscout"]:
                draw_ns_pixel(data["nightscout"])

            # Display
            epd.display(epd.getbuffer(hkdraw.context.image))

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
    epd7in5_V2.epdconfig.module_exit()
    exit()
