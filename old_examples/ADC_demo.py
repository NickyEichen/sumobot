#!/urs/bin/python

import spidev
import time

delay = 0.5
channel = 0

spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
	if adcnum > 7 or adcnum < 0:
		print("Invalid port number")
		return -1
	r = spi.xfer2([1,  8 + adcnum << 4, 0])
	print(r)
	data = ((r[1] & 3) << 8) + r[2]
	return data

while True:
	ldr_value = readadc(channel)
	print("LDR Value: ", ldr_value)
	time.sleep(delay)
