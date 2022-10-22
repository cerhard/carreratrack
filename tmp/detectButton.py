import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import logging 
import contextlib
from carreratrack.carreralib import ControlUnit
import time

###
# GPIO Pins:  
#   10:  Switch
#   16:  Yellow Light
#   18:  Green Light

logging.basicConfig(level=logging.DEBUG,
                filename='carreralib.log',
                format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d,%H:%M:%S')

def turnYellowOn():
    GPIO.output(16,GPIO.HIGH)

def turnYellowOff():
    GPIO.output(16,GPIO.LOW)

def turnGreenOn():
    GPIO.output(18,GPIO.HIGH)

def turnGreenOff():
    GPIO.output(18,GPIO.LOW)

def button_callback(channel):
    print("CAUTION!  Cars will be slow for 10 seconds")
    with contextlib.closing(ControlUnit('/dev/ttyUSB0', timeout=300)) as cu:
        turnYellowOn()
        turnGreenOff()
        for i in range(7):
            cu.setspeed(i,1)

        # Yellow on for 7 seconds
        for i in range(7):
            print("{}".format(10-i))
            time.sleep(1)
        
        for i in range(7,10):
            print("{}".format(10-i))
            turnYellowOff()
            time.sleep(0.5)
            turnYellowOn()
            time.sleep(0.5)

        turnYellowOff()
        turnGreenOn()
        for i in range(7):
            cu.setspeed(i,10)


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

turnYellowOff()
turnGreenOn()
message = input("Press enter to quit\n\n") # Run until someone presses enter

turnYellowOff()
turnGreenOff()

GPIO.cleanup() # Clean up