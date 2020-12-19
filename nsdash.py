#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
from datetime import datetime

import logging
from lib.waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

from nsdata import NSData


logging.basicConfig(level=logging.DEBUG)

def get_time():
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    return datetime.now().strftime("%H:%M")

try:
    logging.info("epd2in13_V2 Demo")

    nsdata = NSData()

    height = 122 #epd.width?
    width = 250 #epd.height?
    black = 0
    white = 1
    image = Image.new('1', (width, height), white)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(os.environ['NSDASH_FONT'], size=42)
    font2 = ImageFont.truetype(os.environ['NSDASH_FONT'], size=20)

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    epd.displayPartBaseImage(epd.getbuffer(image))
    epd.init(epd.PART_UPDATE)

    while True:
        # Retrieve data
        data = nsdata.get_data()
        fvalue = f'{data["sgv"]}{data["direction"]}'
        #fvalue = '%.1f%s' % (value, direction)

        # Draw on image
        draw.rectangle((0, 0, width, height), fill=white)
        draw.text((20, 20), fvalue, font = font, fill = black)
        size = draw.textsize(fvalue, font)
        draw.text((20 + size[0], 20), f'{data["delta"]}\n[{data["minutes_ago"]}m]', font=font2, fill=black)
        
        time_text = get_time()
        time_dim = draw.textsize(time_text, font2)
        draw.text((width - time_dim[0], 0), get_time(), font=font2)

        # Render image
        print(time_text, fvalue)
        epd.displayPartial(epd.getbuffer(image))

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
