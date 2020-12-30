#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from datetime import datetime

import logging
from lib.waveshare_epd import epd2in13_V2

from data.nightscout import NightscoutData
from draw.nsdraw import NSDraw

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V2 Demo")

    height = 122 #epd.width?
    width = 250 #epd.height?

    nsdata = NightscoutData()
    nsdraw = NSDraw(width, height)

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(nsdraw.image))
    epd.init(epd.PART_UPDATE)

    while True:
        # Retrieve data
        data = nsdata.get_data()

        # Once in a while, do a full clear
        if datetime.now().minute == 0:
            logging.info("Periodical full clear")
            epd.init(epd.FULL_UPDATE)
            nsdraw.clear_image()
            epd.displayPartBaseImage(epd.getbuffer(nsdraw.image))
            epd.init(epd.PART_UPDATE)

        # Draw
        nsdraw.draw_data(data)

        # Display
        epd.displayPartial(epd.getbuffer(nsdraw.image.rotate(180)))

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
    #epd2in13_V2.epdconfig.module_exit()
    exit()
