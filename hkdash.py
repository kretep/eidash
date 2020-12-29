#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime
import locale

import logging
from lib.waveshare_epd import epd7in5_V2

from hkdata import HKData
from hkdraw import HKDraw
from nsdata import NSData

logging.basicConfig(level=logging.DEBUG)

try:
    locale.setlocale(locale.LC_TIME, "nl_NL.utf8")

    logging.info("Starting")

    epd = epd7in5_V2.EPD()
    time.sleep(2)
    width = epd.width # 800
    height = epd.height # 480
    print(width, height)

    hkdata = HKData()
    nsdata = NSData()
    hkdraw = HKDraw(width, height)

    logging.info("init and Clear")
    epd.init()
    time.sleep(2)
    epd.Clear()
    time.sleep(2)

    #epd.displayPartBaseImage(epd.getbuffer(hkdraw.image))
    #epd.init(epd.PART_UPDATE)

    while True:
        # Retrieve data
        data = hkdata.get_weather_data()
        data["moonphase"] = hkdata.get_moon_age_fraction()
        nsd = nsdata.get_data()

        # Once in a while, do a full clear
#        if datetime.now().minute == 0:
#            logging.info("Periodical full clear")
#            epd.init(epd.FULL_UPDATE)
#            hkdraw.clear_image()
#            epd.displayPartBaseImage(epd.getbuffer(hkdraw.image))
#            epd.init(epd.PART_UPDATE)

        # Draw
        hkdraw.draw_data(data, nsd)

        # Display
        epd.display(epd.getbuffer(hkdraw.image))

        # Sleep until the next minute
        seconds_to_go = 60 - datetime.now().second
        print("Sleeping for ", seconds_to_go, " seconds")
        time.sleep(seconds_to_go)

    # logging.info("Clear...")
    # epd.init(epd.FULL_UPDATE)
    # epd.Clear(0xFF)
    
    #logging.info("Goto Sleep...")
    #epd.sleep()
    #epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
