#!/usr/bin/python
# -*- coding: utf-8 -*-

from bluetooth.ble import GATTRequester


class Toio(object):
    HANDLER = {'motor': "TBU"}
    DIRECTION = {'fwd': 1, 'bck': 2}
    MOTOR = {'1st': 1, '2nd': 2}
    SPEED_MAX = 100

    def __init__(self, addr):
        self.req = ""
        if not addr:
            return
        self.req = GATTRequester(addr, False)
        print("Connecting...: {}".format(addr))
        self.req.connect(wait=True, channel_type="random")
        print("Connected: {}".format(addr))

    def request_data(self, uuid):
        return self.req.read_by_uuid(uuid)[0]

    def write_data(self, handler, data):
        self.req.write_by_handle(handler, data)

    def disconnect(self):
        self.req.disconnect()

    def is_connected(self):
        if not self.req:
            return False
        return self.req.is_connected()

    def _move(self, motor_1st_dir, motor_1st_speed, motor_2nd_dir, motor_2nd_speed, duration_sec):
        self.write_data(self.HANDLER['motor'], str(
            bytearray([2, self.MOTOR['1st'], motor_1st_dir, motor_1st_speed, self.MOTOR['2nd'], motor_2nd_dir, motor_2nd_speed, int(duration_sec * 100)])))
        import time
        time.sleep(duration_sec)

    def straight(self):
        self._move(self.DIRECTION['fwd'], self.SPEED_MAX, self.DIRECTION['fwd'], self.SPEED_MAX, 1)

    def turn_left(self):
        self._move(self.DIRECTION['fwd'], self.SPEED_MAX / 2, self.DIRECTION['fwd'], self.SPEED_MAX, 1)

    def turn_right(self):
        self._move(self.DIRECTION['fwd'], self.SPEED_MAX, self.DIRECTION['fwd'], self.SPEED_MAX / 2, 1)

    def back(self):
        self._move(self.DIRECTION['bck'], self.SPEED_MAX, self.DIRECTION['bck'], self.SPEED_MAX, 1)

    def spin_turn_180(self):
        self._move(self.DIRECTION['bck'], self.SPEED_MAX, self.DIRECTION['fwd'], self.SPEED_MAX, 0.5)

    def spin_turn_360(self):
        self._move(self.DIRECTION['bck'], self.SPEED_MAX, self.DIRECTION['fwd'], self.SPEED_MAX, 1)
