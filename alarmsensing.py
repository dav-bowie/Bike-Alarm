from hcsr04 import HCSR04
from machine import Pin, I2C, PWM, Timer
import time
from time import sleep
from board import LED
import math

# Establish wifi connection
from mqttclient import mqttclient
import network
import sys

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print('no wifi connection')
    sys.exit()
else:
    print("connected to Wifi at IP", ip)

# Set up Adafruit
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'OskiBear'
adafruitAioKey = ''
feedName = "OskiBear/feeds/door-alarm-project"

# Connect to adafruit
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user='OskiBear', password='')
time.sleep(0.5)
print("Connected!")

# Subscribe to the feed
mqtt.subscribe(feedName)

# Set up the ultrasonic sensor
ultrasonic = hcsr04.HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=1000000)

# Set up the buzzer/speaker
led = Pin(LED, mode=Pin.OUT)
pin = Pin(27, mode=Pin.OUT)
buzzer = PWM(pin,freq=4186, duty=150, timer=0)

#Define function
while True:
    distance = ultrasonic.distance_cm()
    print('Distance:', distance, 'cm')
    if distance >= 5:
        buzzer.duty(512)
        led.on()
    else:
        buzzer.duty(0)
        led.off()
    time.sleep_ms(1000)

# Publish message to Adafruit
mqtt.publish(feedName,str(distance))
print("Published {} to {}.".format(message,feedName))

try:
    while True:
        mqtt.check_msg()
except KeyboardInterrupt:
        pass
