"""
!/usr/bin/env python3
This Python file uses the following encoding: utf-8

GPL-3.0 license

OLED advanced stats display script for RaspberryPi
"""

# Standard modules
from datetime import datetime
import logging
import os
import sys
from time import sleep
import re

# Insatlled modules via pip
import yaml
from gpiozero import Button

# Project related modules
from modules.buttons import Buttons
from modules.buttonsfunc import ButtonsFunc
from modules.pages import Pages

# Will be set in load_config()
BUTTON = None
# Sleep time in seconds (Sleep this script for the specified time)
SLEEP_TIME = 0.1

# Logging
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = os.path.basename(__file__)
os.makedirs(DIR_PATH + "/logs", exist_ok=True)
now = datetime.now()
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(lineno)-4d %(funcName)s(): %(message)s",
    filename=DIR_PATH + "/logs/%s.log" % (now.strftime("%Y_%m_%d")),
    datefmt="%H:%M:%S",
    level=logging.ERROR,
    # level=logging.DEBUG,
)
LOGGER = logging.getLogger(__name__)
LOGGER.debug("")
LOGGER.debug("Python script has started")


def load_config():
    """Load configuration"""
    # Load configuraton file
    if not os.path.exists(DIR_PATH + '/config.yml'):
        e = 'No config found!'
        LOGGER.error(e)
        sys.exit(e)
    try:
        with open(DIR_PATH + '/config.yml', 'r', encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except Exception as e:
        LOGGER.exception(e)
        sys.exit(e)
    if config is None:
        e = 'Config is not a yaml file!'
        LOGGER.error(e)
        sys.exit(e)

    # Load oled configuration
    if not 'oled' in config:
        e = 'Config does not contain a \'oled\' paragraph!'
        LOGGER.error(e)
        sys.exit(e)
    config_oled = config['oled']
    if not 'i2c_port' in config_oled:
        e = 'Config paragraph \'oled\' does not contain a \'i2c_port\' key!'
        LOGGER.error(e)
        sys.exit(e)
    if not 'i2c_address' in config_oled:
        e = 'Config paragraph \'oled\' does not contain a \'i2c_address\' key!'
        LOGGER.error(e)
        sys.exit(e)
    if not 'driver' in config_oled:
        e = 'Config paragraph \'oled\' does not contain a \'driver\' key!'
        LOGGER.error(e)
        sys.exit(e)
    Pages.setDevice(config_oled['i2c_port'],
                    config_oled['i2c_address'],
                    config_oled['driver'])

    # Load main configuration
    if not 'main' in config:
        e = 'Config does not contain a \'main\' paragraph!'
        LOGGER.error(e)
        sys.exit(e)
    config_main = config['main']
    if not 'mode' in config_main:
        e = 'Config paragraph \'main\' does not contain a \'mode\' key!'
        LOGGER.error(e)
        sys.exit(e)
    if not 'showicons' in config_main:
        e = 'Config paragraph \'main\' does not contain a \'showicons\' key!'
        LOGGER.error(e)
        sys.exit(e)
    if not Pages.set_show_icons(config_main['showicons']):
        e = 'Config paragraph \'main\' key \'showicons\' is not setup correctly!'
        LOGGER.error(e)
        sys.exit(e)
    if 'auto' in config_main['mode']:
        Pages.set_mode(config_main['mode'])
        if not 'autodelay' in config_main:
            e = 'Config paragraph \'main\' does not contain a \'autodelay\' key!'
            LOGGER.error(e)
            sys.exit(e)
        if not Pages.set_auto_delay(config_main['autodelay']):
            e = 'Config paragraph \'main\' key \'autodelay\' is not a number!'
            LOGGER.error(e)
            sys.exit(e)
    elif 'manual' in config_main['mode']:
        Pages.set_mode(config_main['mode'])
        if not 'screensaver' in config_main:
            e = 'Config paragraph \'main\' does not contain a \'screensaver\' key!'
            LOGGER.error(e)
            sys.exit(e)
        if not Pages.Screensaver.set(config_main['screensaver']):
            e = 'Config paragraph \'main\' key \'screensaver\' is not a number!'
            LOGGER.error(e)
            sys.exit(e)
    else:
        e = 'Config paragraph \'main\' key \'mode\' is not setup correctly!'
        LOGGER.error(e)
        sys.exit(e)

    # Load pages configuration
    if not 'pages' in config:
        e = 'Config does not contain a \'pages\' paragraph!'
        LOGGER.error(e)
        sys.exit(e)
    for config_page in config['pages']:
        if not 'type' in config_page:
            e = 'Config paragraph \'pages\' is not setup correctly!'
            LOGGER.error(e)
            sys.exit(e)
        if not config_page['type'].lower() in Pages.requirements():
            e = 'Config paragraph \'pages\' is not setup correctly!'
            LOGGER.error(e)
            sys.exit(e)
        if 'simple' in Pages.requirements()[config_page['type'].lower()]['pointer']:
            if 'icon' in config_page:
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            if 'value' in config_page:
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            ptr = Pages.str_to_ptr(config_page['type'].lower())
            if ptr:
                Pages.add({
                    'ptr': ptr,
                    'args': None
                })
        if 'advanced' in Pages.requirements()[config_page['type'].lower()]['pointer']:
            if not 'icon' in config_page:
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            if not 'value' in config_page:
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            if not config_page['icon'] in Pages.requirements()[config_page['type'].lower()]['icons']:
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            if not re.match(Pages.requirements()[config_page['type'].lower()]['values'], config_page['value']):
                key = config_page['type'].lower()
                e = f'Config paragraph \'pages\' key \'{key}\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            ptr = Pages.str_to_ptr(config_page['type'].lower())
            if ptr:
                Pages.add({
                    'ptr': ptr,
                    'args': {'icon': config_page['icon'], 'value': config_page['value']}
                })

    # Load buttons configuration
    if 'manual' in config_main['mode']:
        if not 'buttons' in config:
            e = 'Config does not contain a \'buttons\' paragraph!'
            LOGGER.error(e)
            sys.exit(e)
        if config['buttons'] is None:
            e = 'You need to setup at least one push button!'
            LOGGER.error(e)
            sys.exit(e)
        for config_buttons in config['buttons']:
            if not 'gpio' or not 'func' in config_buttons:
                e = 'Config paragraph \'buttons\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            try:
                GPIO = abs(int(config_buttons['gpio']))
            except Exception:
                e = 'Config paragraph \'buttons\' key \'gpio\' is not a number!'
                LOGGER.error(e)
                sys.exit(e)
            if 'next' in config_buttons['func']:
                FUNC = ButtonsFunc.next_pressed_func
            elif 'previous' in config_buttons['func']:
                FUNC = ButtonsFunc.previous_pressed_func
            else:
                e = 'Config paragraph \'buttons\' key \'func\' is not setup correctly!'
                LOGGER.error(e)
                sys.exit(e)
            Buttons.add(GPIO,
                        pull_up=True,
                        active_state=None,
                        bounce_time=0.050,
                        when_released=FUNC)


def main():
    """Main programm"""
    try:
        load_config()
    except Exception as e:
        LOGGER.exception(e)

    while True:
        try:
            Pages.show()
            sleep(SLEEP_TIME)
        except Exception as e:
            LOGGER.exception(e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
