## make longer tones and remove looping

import serial

import pygame, time
from pygame.locals import *
import os

sensor_port = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo_HIDPC-if00'
baud = 9600
sensors = serial.Serial(sensor_port, baud, timeout = 0)


#sound samples
SAMPLE_FOLDER = "samples/tones"

#load samples

BANK = os.path.join(os.path.dirname(__file__), SAMPLE_FOLDER)

pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)

#http://www.audiocheck.net/audiofrequencysignalgenerator_sinetone.php
tones = { 100: "audiocheck.net_sin_100Hz_-3dBFS_1s.wav",
          200: "audiocheck.net_sin_200Hz_-3dBFS_1s.wav",
          300: "audiocheck.net_sin_300Hz_-3dBFS_1s.wav",
          400: "audiocheck.net_sin_400Hz_-3dBFS_1s.wav",
          500: "audiocheck.net_sin_500Hz_-3dBFS_1s.wav"}



toneSounds = dict()
for key, sound in tones.items():
    t= os.path.join(BANK, sound)
    s= pygame.mixer.Sound( t )
    toneSounds[key] = s
print toneSounds    

lasttone=100
tone=100 

while True:
    input = sensors.readline()
    input = input.replace('\n', '')
    input = input.replace('\r', '')
    if(input != ""):
            values = input.split("#")
            flex = int(values[0])
            force = values[1]
            print flex

            if 0 <= flex <= 10:
                toneSounds[tone].fadeout(100)
                pass
            if 11 <= flex <= 20:
                tone = 100
            if 21 <= flex <= 40:
                tone = 200
            if 41 <= flex <= 60:
                tone = 300
            if 61 <= flex <= 70:
                tone = 400
            if 71 <= flex <= 80:
                tone = 500
            if tone != lasttone:
                toneSounds[lasttone].fadeout(100)
                toneSounds[tone].play(loops=-1)
                lasttone=tone



            



