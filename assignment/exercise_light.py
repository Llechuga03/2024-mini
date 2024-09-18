#!/usr/bin/env python3
"""
Use analog input with photoresistor to control the apparent brightness of the LED.
"""

import time
import machine

ADC2 = 28

led = machine.Pin("LED", machine.Pin.OUT)
adc = machine.ADC(ADC2)

blink_period = 0.1

max_bright = 17000
min_bright = 10000


def clip(value: float) -> float:
    """Clip number to range [0, 1]"""
    if value < 0:
        return 0
    if value > 1:
        return 1
    return value

while True:
    value = adc.read_u16()
    print(value)

    duty_cycle = clip((value - min_bright) / (max_bright - min_bright))

    if duty_cycle == 0:
       
        led.low()
    else:
        led.high()
        time.sleep(blink_period * duty_cycle)

        led.low()
        time.sleep(blink_period * (1 - duty_cycle))
