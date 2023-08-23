import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

class LightSensor:

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    all = []
    lookup_port = {0: MCP.P0, 1: MCP.P1, 2: MCP.P2, 3:MCP.P3, 4:MCP.P4, 5:MCP.P5, 6:MCP.P6, 7:MCP.P7}

    light_pin = 0

    def __init__(self, port):
        self.channel = AnalogIn(self.mcp, self.lookup_port[port])
        self.min = 0
        self.max = 3.3
        self.all.append(self)

    def read_raw(self):
        return float(self.channel.value)

    def read(self):
        return self.minmax((self.read_raw() - self.min) / (self.max - self.min))

    def set_low(self):
        self.min = self.read_raw()

    def set_high(self):
        self.max = self.read_raw()

    @staticmethod
    def save_values():
        pass

    @staticmethod
    def turn_light_on():
        pass

    @staticmethod
    def turn_light_off():
        pass

    @staticmethod
    def minmax(val, low=0, high=1):
        return max(low, min(high, val))
