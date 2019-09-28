#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import termios
import tty

from toio.toio import Toio

UUID_NAME = "10B20100-5B3B-4571-9508-CF3EFCD7BBAE"


class ReadChar():

    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


def _get_ta_addr():
    from pygatt.backends.gatttool.gatttool import GATTToolBackend
    gatttool = GATTToolBackend()
    devices = gatttool.scan(timeout=5)
    ret_addr = ""

    for d in devices:
        if d['name'] and 'toio Core Cube' in d['name']:
            print("Toio name: {}, address: {}".format(d['name'], d['address']))
            ret_addr = d['address']
    if not ret_addr:
        print("Toio not found")
    return str(ret_addr)


def main():
    toio = Toio(_get_ta_addr())
    if toio.is_connected():
        toio.request_data(UUID_NAME)
        toio.straight()
        toio.disconnect()


def main_steps():
    toio = Toio(_get_ta_addr())
    if toio.is_connected():
        toio.straight()
        toio.turn_right()
        toio.back()
        toio.spin_turn_180()
        toio.disconnect()


def main_user_input():
    toio = Toio(_get_ta_addr())
    if toio.is_connected():
        print("w: UP, a: TURN LEFT, d: TURN RIGHT, x: BACK, SHIFT+C: exit")
        while True:
            with ReadChar() as rc:
                char = rc
            if char == 'w':
                toio.straight()
            elif char == 'a':
                toio.turn_left()
            elif char == 'd':
                toio.turn_right()
            elif char == 'x':
                toio.back()
            if char in "^C":
                break
        toio.disconnect()


def main_test():
    toio = Toio(_get_ta_addr())
    if toio.is_connected():
        toio.back()
        toio.disconnect()


if __name__ == '__main__':
    # main()
    # main_steps()
    main_user_input()
    # main_test()
