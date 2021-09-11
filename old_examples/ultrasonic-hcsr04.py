#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: May 8th, 2020
# Version: 1.0

# Import required libraries
import RPi.GPIO as GPIO
import time

# --------------------------------------------------------------------
# PINS MAPPING AND SETUP
# --------------------------------------------------------------------

echoPIN = 21
triggerPIN = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(echoPIN,GPIO.IN)
GPIO.setup(triggerPIN,GPIO.OUT)
GPIO.setwarnings(True)

# --------------------------------------------------------------------
# MAIN FUNCTIONS
# --------------------------------------------------------------------

def distance ():
 distance = 0
 duration = 0

 # send trigger
 GPIO.output(triggerPIN, 0)
 time.sleep(0.000002)
 GPIO.output(triggerPIN, 1)
 time.sleep(0.000010)
 GPIO.output(triggerPIN, 0)
 time.sleep(0.000002)

 # wait for echo reading
 while GPIO.input(echoPIN) == 0: pass
 startT = time.time()
 while GPIO.input(echoPIN) == 1: pass
 feedbackT = time.time()

 # calculating distance
 if feedbackT == startT:
  distance = "N/A"
 else:
  duration = feedbackT - startT
  soundSpeed = 34300 # cm/s
  distance = duration * soundSpeed / 2
  distance = round(distance, 1)
 time.sleep(0.2)
 return distance

# --------------------------------------------------------------------
# MAIN LOOP
# --------------------------------------------------------------------
print("Starting...")
try:
 while True:
  print (" Distance: " + str(distance())+ "   ", end='\r')
except KeyboardInterrupt:
 print('interrupted!')
 GPIO.cleanup()


