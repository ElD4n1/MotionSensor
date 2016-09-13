import RPi.GPIO as GPIO
import time
import threading
from indoorpersontrackerapi import IndoorPersonTrackerAPI
from configparser import ConfigParser

def sensorloop(gpio_pin, identifier, prob_false_detection):
    while True:
        i=GPIO.input(gpio_pin)
        if i==1:                 #When output from motion sensor is HIGH
             print("{}: Motion detected".format(identifier))
             tracker.updateDetection(identifier, prob_false_detection)
             time.sleep(1.5) # sleep longer to not detect the same person too often
        else:
             time.sleep(0.1)

class SensorThread (threading.Thread):
    def __init__(self, gpio_pin, identifier, prob_false_detection):
        threading.Thread.__init__(self)
        self.gpio_pin = gpio_pin
        self.identifier = identifier
        self.prob_false_detection = prob_false_detection
    def run(self):
        print("Started thread for sensor on pin {}".format(self.gpio_pin))
        tracker.register(self.identifier)
        sensorloop(self.gpio_pin, self.identifier, self.prob_false_detection)

config = ConfigParser()
config.read('config.ini')

tracker = IndoorPersonTrackerAPI()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

for sensor in config.sections():
    try:
        GPIO.setup(int(config[sensor]['GPIO_PIN']), GPIO.IN)         #Read output from PIR motion sensor
        sensorthread = SensorThread(int(config[sensor]['GPIO_PIN']), config[sensor]['IDENTIFIER'], float(config[sensor]['PROB_FALSE_DETECTION']))
        sensorthread.start()
    except Exception as error:
        print("unable to start thread: {}".format(error))
