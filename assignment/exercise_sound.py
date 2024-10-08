#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)

# Death Song from Mario
# (Freq,duration)
mario = [
    (523,0.25),(0,0.1),
    (523,0.25),(0,0.1),
    (523,0.25),(0,0.1),
    (294,0.25),(0,0.05),
    (330,0.25),(0,0.05),
    (330,0.25),(0,0.05),
    (349,0.25),(0,0.3),
    (392,0.25),(0,0.3),
    (440,0.25),(0,0.05),
    (494,0.25),(0,0.05),
]
# we don't need this
#freq: float = 30
#duration: float = 0.1  # seconds

print("Playing Mario Death Song:")

# loops through the mario notes
for i, dur in mario:
    #for pauses
    if i == 0
        quiet()
    # to play notes
    else
        playtone(i,dur)

# Turn off the PWM
quiet()
