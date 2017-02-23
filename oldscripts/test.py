import serial
sensor_port = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo_HIDPC-if00'
baud = 9600
sensors = serial.Serial(sensor_port, baud, timeout = 0)



import pygame
from pygame.locals import *

import math
import numpy

size = (1366, 720)

bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)





duration = 0.1          # in seconds
#freqency for the left speaker
frequency_l = 200 
#frequency for the right speaker
frequency_r = 200

sample_rate = 44100
n_samples = int(round(duration*sample_rate))
#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
max_sample = 2**(bits - 1) - 1

for s in range(n_samples):
    t = float(s)/sample_rate    # time in seconds

    #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
    buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
    buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right
sound = pygame.sndarray.make_sound(buf)
sound.play(loops = -1)




#This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
_running = True
while _running:
    input = sensors.readline()
    input = input.replace('\n', '')
    input = input.replace('\r', '')
    if(input != ""):
            values = input.split("#")
            flex = values[0]
            force = values[1]
            #print flex




    duration = 0.1          # in seconds
    #freqency for the left speaker
    frequency_l = 200 + (int(flex) *2)
    #frequency for the right speaker
    frequency_r = 200 + (int(flex) *2)

    sample_rate = 44100
    n_samples = int(round(duration*sample_rate))
    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(bits - 1) - 1

    for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds

        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
        buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right
    sound.stop()
    sound = pygame.sndarray.make_sound(buf)

    

    #play once, then loop forever
    sound.play(loops = -1)



        



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break

pygame.quit()
