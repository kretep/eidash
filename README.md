# Nightscout Dashboard
Shows [Nightscout](http://www.nightscout.info) data on a [Waveshare](https://www.waveshare.com) e-Paper display.

Based on:
nightscout-osx-menubar: https://github.com/mddub/nightscout-osx-menubar
waveshare e-paper demos: https://github.com/waveshare/e-Paper

## Hardware

I have this running on a Raspberry Pi Zero W running Raspbian Buster, with a [2.13 inch (v2) e-Paper display](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT). The code can easily be adapted for other displays.

## Install prerequisites
This project assumes you're using Python 3.

```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install ephem
```

Do not install pil and numpy with pip, as these do not install some required native libraries.

It doesn't seem there is an up-to-date packaged distribution of the waveshare epd libraries, so lib/waveshare_epd is simply a copy of the libraries at https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd

## Enable SPI
In `sudo raspi-config` > Interface options > SPI, enable SPI.

## Make sure you have fonts
If you are running headless, your system likely has no fonts. Download some here: https://dejavu-fonts.github.io/

Otherwise, fonts will probably be located in /usr/share/fonts/truetype/dejavu/

## Set up environment variables
Doesn't matter where you do this, /etc/environment is a convenient place. These are required:

```
export NSDASH_URL=<your nightscout site>
export NSDASH_FONT=<path to your font file>
export HKDASH_WL_KEY=<weerlive API key>
export HKDASH_WL_LOCATION=<weerlive location>
```

## Install locale

List installed locales: `locale -a`

Generate locales:
```
sudo dpkg-reconfigure locales
```
Use space bar to select, use None for default.

## Connect e-Paper HAT with wires

See https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT > Hardware/Software setup
and https://pinout.xyz/

HAT|RPI BCM2835|RPI Board
:---: | :---: | :---:
VCC|3.3V|3.3V
GND|GND|GND
DIN|MOSI|Pin 19
CLK|SCLK|Pin 23
CS|CE0|Pin 24
DC|GPIO 25|Pin 22
RST|GPIO 17|Pin 11
BUSY|GPIO 24|Pin 18
