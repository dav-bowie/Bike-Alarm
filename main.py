from hcsr04 import HCSR04
from machine import Pin, I2C, PWM, Timer
import time
from time import sleep
from board import LED
import math

from mqttclient import MQTTClient
import network
import sys
import time


# Establish Internet con nection
from network import WLAN, STA_IF
from network import mDNS
import time 

wlan = WLAN(STA_IF)
wlan.active(True)

wlan.connect('ME100-2.4G', '122Hesse', 5000)

tries = 0
while not wlan.isconnected() and tries < 10:
    print("Waiting for wlan connection")
    time.sleep(1)
    tries = tries + 1

if wlan.isconnected():
        print("WiFi connected at", wlan.ifconfig()[0])
else:
        print("Unable to connect to WiFi")

# Advertise as 'hostname', alternative to IP address
try:
    hostname = "david's ESP32"
    mdns = mDNS(wlan)
    # mdns.start(hostname, "MicroPython REPL")
    # mdns.addService('_repl', '_tcp', 23, hostname)
    mdns.start(hostname,"MicroPython with mDNS")
    _ = mdns.addService('_ftp', '_tcp', 21, "MicroPython", {"board": "ESP32", "service": "my_hostname FTP File transfer", "passive": "True"})
    _ = mdns.addService('_telnet', '_tcp', 23, "MicroPython", {"board": "ESP32", "service": "my_hostname Telnet REPL"})
    _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "my_hostname Web server"})
    print("Advertised locally as {}.local".format(hostname))

except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

print("start telnet server")
telnet.start(user='', password='')

# fetch NTP time
from machine import RTC

print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 10
for _ in range(timeout):
    if rtc.synced():
        break
    print("Waiting for rtc time")
    time.sleep(1)

if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("could not get NTP time")






wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = ''
adafruitAioKey = ''

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='', user='', password='')
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

# Send test message
feedName = "/feeds/alarm"
testMessage = "Bike is stolen!"

# testMessage = "1"

#when bike is not stolen
testMessage1 = "Bike is Safe!"

# For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
# for i in range(0, 60):
#     mqtt.check_msg()
#     time.sleep(1)




## code for blinking

from board import LED
from machine import Pin
import time

# ## lab6 mock
#
# led=Pin(33, mode=Pin.OUT)
# brightness = 50
# L1 =PWM(led,freq=500,duty=brightness,timer=0)
#
# ##



#Initialize built in LED pin
led  =  Pin(LED,  mode=Pin.OUT)
counter = 0
while (counter < 3):
    led(1)
    time.sleep(0.5)
    led(0)
    time.sleep(0.5)
    counter = counter+1

# led2 = Pin(LED,  mode=Pin.OUT)
# counter = 0
# while (counter < 2):
#     led(1)
#     time.sleep(0.5)
#     led(0)
#     time.sleep(0.5)
#     counter = counter+1


##
# Set up the ultrasonic sensor
ultrasonic = HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=1000000)

# Set up the buzzer/speaker
led = Pin(LED, mode=Pin.OUT)
buz = Pin(33, mode=Pin.OUT)


# This is just for the buzzer
# led1 = Pin(LED, mode=Pin.OUT)
# buzzer = Pin(27, mode=Pin.OUT)



#pin = Pin(27, mode=Pin.OUT)
#buzzer = PWM(27,freq=4186, duty=0, timer=0)

# L1 = PWM(Pin(5)) # you can use other pins! and connect to ground
# L1.duty(0)
# led=Pin(27, mode=Pin.OUT)
# brightness = 50
# L1 =PWM(led,freq=500,duty=brightness,timer=0)
# def tcb(timer):
# 	L1.freq(1000)


    ## Code for when bike is stolen; alerts the user



    # Check wifi connection



#Define function
while True:
    distance = ultrasonic.distance_cm()
    print('Distance:', distance, 'cm')
    if distance >= 7:
        #buzzer.duty(100)
        buz(1)
        # t1=Timer(1)
        # t1.init(period=250, mode=t1.PERIODIC, callback=tcb)
        #led.on()
        print('Bike Is Stolen')
        time.sleep(10)
        mqtt.publish(feedName,testMessage)
        print("Published {} to {}.".format(testMessage,feedName))

        mqtt.subscribe(feedName)

    else:
        #buzzer.duty(0)
        buz(0)

        #led.off()
        print("Bike is Safe")
        time.sleep(10)
        mqtt.publish(feedName,testMessage1)
        print("Published {} to {}.".format(testMessage1,feedName))
        mqtt.subscribe(feedName)
    # time.sleep_ms(1000)
## _______________ ##
