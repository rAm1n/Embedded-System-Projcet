
from Adafruit.Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO

# GPIO BCM Mode I/O pins number
# LEDs
RED = 3
GREEN = 9
BLUE = 2
MS = 25 # Motion sensor

# GPIO Setup
GPIO.setmode(GPIO.BCM)
# outputs
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
#inputs
GPIO.setup(MS, GPIO.IN)

# lcd setup
lcd = Adafruit_CharLCD()
lcd.begin(16, 2)

lcd.message("Hello World!")