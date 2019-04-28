from typing import List
import wiringpi

DEFAULT_STATUS = {
    "type": "INPUT",
    "pull_up_dn": "PULL_DOWN",
    "value": "UNSPECIFIED"
}


def init_pin(pin):
    return GpioPin(pin, DEFAULT_STATUS)


class GpioController:
    def __init__(self):
        wiringpi.wiringPiSetupGpio()
        self.pins = {}

    def init_pins(self, wiringpi_pins: List[int]):
        self.pins = {pin: init_pin(pin) for pin in wiringpi_pins}


class GpioPin:
    def __init__(self, pin, default_status):
        self.pin = pin
        self.type = None
        self.pull_up_dn = None
        self.value = None

        self.set_status(default_status)

    def set_status(self, status):
        self.set_type(status['type'])
        self.set_pull_resistor(status['type'])
        self.set_value(status['value'])

    def get_status(self):
        return {
            'type': self.type,
            'pull_up_down': self.pull_up_dn,
            'value': self.get_value()
        }

    def get_value(self):
        if self.type != 'OUTPUT':
            return 'UNSPECIFIED'

        wiringpi_value = wiringpi.digitalRead(self.pin)
        if wiringpi_value == wiringpi.HIGH:
            return "HIGH"
        else:
            return "LOW"

    def set_value(self, value):
        if value != self.value:
            if self.type != 'OUTPUT' and value != 'UNSPECIFIED':
                raise Exception('Values can be only set for output pins')

            if value == 'HIGH':
                wiringpi.digitalWrite(self.pin, wiringpi.HIGH)
            elif value == 'LOW':
                wiringpi.digitalWrite(self.pin, wiringpi.LOW)

            self.value = value

    def set_type(self, pin_type):
        if pin_type != self.type:
            mode = None
            if pin_type == 'INPUT':
                mode = 0
            elif pin_type == 'OUTPUT':
                mode = 1
            wiringpi.pinMode(self.pin, mode)

            self.type = pin_type

    def set_pull_resistor(self, pull_resistor):
        if pull_resistor != self.pull_up_dn:

            if self.type != 'INPUT' and pull_resistor != 'OFF':
                raise Exception('Pull resistor can be only used for input pins')

            if pull_resistor == 'PULL_UP':
                wiringpi.pullUpDnControl(self.pin, wiringpi.PUD_UP)
            elif pull_resistor == 'PULL_DOWN':
                wiringpi.pullUpDnControl(self.pin, wiringpi.PUD_DOWN)
            else:
                wiringpi.pullUpDnControl(self.pin, wiringpi.PUD_OFF)

            self.pull_up_dn = pull_resistor
