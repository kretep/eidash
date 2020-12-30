#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import locale

import logging
from lib.waveshare_epd import epd7in5_V2

from draw.hkdraw import HKDraw
from data.nightscout import NightscoutData
from data.weather import WeatherData
from data.ephem import EphemData

logging.basicConfig(level=logging.DEBUG)

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

    logging.info("Starting")

    epd = epd7in5_V2.EPD()
    width = epd.width # 800
    height = epd.height # 480

    nightscoutData = NightscoutData()
    weatherData = WeatherData()
    ephemData = EphemData()
    hkdraw = HKDraw(width, height)

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    while True:
        # Retrieve data
        data = {
            "nightscout": nightscoutData.get_data(),
            "weather": weatherData.get_data(),
            "ephem": ephemData.get_data()
        }

        # Draw
        hkdraw.draw_data(data)

        # Display
        epd.display(epd.getbuffer(hkdraw.image))

        # Sleep until the next minute
        seconds_to_go = 60 - datetime.now().second
        print("Sleeping for ", seconds_to_go, " seconds")
        time.sleep(seconds_to_go)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
