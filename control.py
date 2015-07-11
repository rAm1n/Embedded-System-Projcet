
from time import sleep, strftime
from subprocess import *
from datetime import datetime
import threading

import RPi.GPIO as GPIO
from matrixKeypad_RPi_GPIO import keypad
from Adafruit.Adafruit_CharLCD import Adafruit_CharLCD

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

# keypad setup
kp = keypad()

def run_cmd(cmd):
  p = Popen(cmd, shell=True, stdout=PIPE)
  output = p.communicate()[0]
  return output

def read_from_keypad():
  s = ''
  while True:
    r = kp.getKey()
    if r != None:
      if r == '#':
        return s
      else:
        s += str(r)

def door_controller():
  while True:
    r = kp.getKey()
    if r == '*':
      lcd.message("Enter the key and then press #")
      key = read_from_keypad()
      if key == door_key:
        GPIO.output(GREEN, 1)
        GPIO.output(RED, 0)
      else:
        GPIO.output(GREEN, 0)
        GPIO.output(RED, 1)
  
def email_notifier():
  pass

def twitter_feed():
  pass

def telegram_feed():
  pass

def internet_flag():
  cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
  ip_addr = run_cmd(cmd)
  while True:
    if ip_addr:
      lcd.message("Connected to internet")
      lcd.message("IP: %s" %ip_addr)
      break
    else:
      lcd.message("No internet connection")
      sleep(10)

if __name__ == "__main__":
  threading.Thread(target=door_controller)
  threading.Thread(target=email_notifier)
  threading.Thread(target=twitter_feed)
  threading.Thread(target=telegram_feed)
  threading.Thread(target=internet_flag)
