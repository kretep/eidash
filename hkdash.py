#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import locale

import logging
from lib.waveshare_epd import epd7in5_V2

from data.nightscout import NightscoutData
from data.weather import WeatherData
from data.ephem import EphemData
from data.birthdays import BirthdayData
from data.sunspots import SunspotData
from data.sunspot_number import SunspotNumber

from draw.hkdraw import HKDraw
from pixel.nightscout_pixel import draw_ns_pixel

logging.basicConfig(level=logging.DEBUG)

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

    logging.info("Starting")
    epd = epd7in5_V2.EPD()
    width = epd.width # 800
    height = epd.height # 480

    logging.info("Init")
    epd.init()

    nightscoutData = NightscoutData()
    weatherData = WeatherData()
    ephemData = EphemData()
    birthdayData = BirthdayData()
    sunspotData = SunspotData()
    sunspotNumber = SunspotNumber()
    hkdraw = HKDraw(width, height)

    while True:
        # Retrieve data
        data = {
            "nightscout": nightscoutData.get_data(),
            "weather": weatherData.get_data(),
            "ephem": ephemData.get_data(),
            "birthdays": birthdayData.get_data(),
            "sunspots": sunspotData.get_data(),
            "sunspot_number": sunspotNumber.get_data()
        }

        # Draw
        hkdraw.draw_data(data)

        # Pixel
        draw_ns_pixel(data["nightscout"])

        # Display
        epd.display(epd.getbuffer(hkdraw.context.image))

        # Sleep until the next update
        now = datetime.now()
        minutes_to_go = 4 - now.minute % 5
        seconds_to_go = 60 - now.second + minutes_to_go * 60
        print("Sleeping for ", seconds_to_go, " seconds")
        time.sleep(seconds_to_go)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
