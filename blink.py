from board import LED
from machine import Pin
import time


#Initialize built in LED pin
led  =  Pin(LED,  mode=Pin.OUT)
counter = 0
while (counter < 3):
    led(1)
    time.sleep(0.5)
    led(0)
    time.sleep(0.5)
    counter = counter+1

led2 = Pin(LED,  mode=Pin.OUT)
counter = 0
while (counter < 2):
    led(1)
    time.sleep(0.5)
    led(0)
    time.sleep(0.5)
    counter = counter+1
