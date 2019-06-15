#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import termios
import tty

from toio import Trolley

UUID_NAME = "TBD"


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
    devices = gatttool.scan(timeout=2)
    ret_addr = ""
    for d in devices:
        if d['name'] and 'Trolley' in d['name']:
            print("TA name: {}, address: {}".format(d['name'], d['address']))
            ret_addr = d['address']
    if not ret_addr:
        print("TA not found")
    return str(ret_addr)


def main():
    trolley = Trolley(_get_ta_addr())
    if trolley.is_connected():
        trolley.request_data(UUID_NAME)
        trolley.straight()
        trolley.disconnect()


def main_steps():
    trolley = Trolley(_get_ta_addr())
    if trolley.is_connected():
        trolley.straight()
        trolley.turn_right()
        trolley.back()
        trolley.spin_turn_180()
        trolley.disconnect()


def main_user_input():
    trolley = Trolley(_get_ta_addr())
    if trolley.is_connected():
        print("w: UP, a: TURN LEFT, d: TURN RIGHT, x: BACK, SHIFT+C: exit")
        while True:
            with ReadChar() as rc:
                char = rc
            if char == 'w':
                trolley.straight()
            elif char == 'a':
                trolley.turn_left()
            elif char == 'd':
                trolley.turn_right()
            elif char == 'x':
                trolley.back()
            if char in "^C":
                break
        trolley.disconnect()


def main_test():
    trolley = Trolley(_get_ta_addr())
    if trolley.is_connected():
        trolley.back()
        trolley.disconnect()


if __name__ == '__main__':
    # main()
    # main_steps()
    main_user_input()
    # main_test()
