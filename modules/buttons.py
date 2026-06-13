"""
!/usr/bin/env python3
This Python file uses the following encoding: utf-8
"""


# Standard modules
from time import time

# Additional pip modules
from gpiozero import Button


class Buttons:
    """Class Button"""
    __buttons = []

    @staticmethod
    def total():
        """Return __buttons length"""
        return len(Buttons.__buttons)

    @staticmethod
    def add(pin=None, *,
            pull_up=True,
            active_state=None,
            bounce_time=None,
            when_released=None):
        """Add new button to list"""
        button = Button(pin,
                        pull_up=pull_up,
                        active_state=active_state,
                        bounce_time=bounce_time)
        if when_released != None:
            button.when_released = when_released
        Buttons.__buttons.append(button)
