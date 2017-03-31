#tasks

#custom inputs - linked to one dreamer nano
#save to file
#load from file
#webserver to edit file
# map key to function


#sound to headphone not hdmi
#amixer cset numid=3 1 (2 for hdmi, 0 for auto)
#sounds from https://www.freesound.org/people/jobro/packs/2489/

import serial

import pygame, time
from pygame.locals import *
import os
import glob
import csv
from collections import OrderedDict
#from threading import Thread
import thread
#from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO





#function buttons
RECORD = 273 # 
PLAY = 276 # 
PLAY_NO_LIGHT = 275

#map keys to sounds
#picade
#1 306
#2 308
#3 32
#4 304
#5 122
#6 120

#left 276
#right 275
#down 274
#up 273

#1up 115
#1/4 99
#esc 27
#ent 13

#makey makey
#W 119
#A 97
#S 115
#D 100
#F 102
#G 103

kb = False #easier keyboard map for testing without device
if(kb):
    buttons = { 113: "000_base.wav",
                119: "001_cowbell.wav",
                101: "002_clash.wav",
                114: "003_whistle.wav",
                116: "004_rim.wav",
                121: "005_hat.wav",
                97 : "39172__jobro__piano-ff-025.wav",
                115: "39174__jobro__piano-ff-027.wav",
                100: "39176__jobro__piano-ff-029.wav",
                102: "39178__jobro__piano-ff-031.wav",
                103: "39180__jobro__piano-ff-033.wav",
                104: "39182__jobro__piano-ff-035.wav"}
else: 
    buttons = { #arcade buttons connected to picade
                306: "000_base.wav",
                308: "001_cowbell.wav",
                32 : "002_clash.wav",
                304: "003_whistle.wav",
                122: "004_rim.wav",
                120: "005_hat.wav",
                #makey makey touch keys
                119: "39172__jobro__piano-ff-025.wav",
                97 : "39174__jobro__piano-ff-027.wav",
                115: "39176__jobro__piano-ff-029.wav",
                100: "39178__jobro__piano-ff-031.wav",
                102: "39180__jobro__piano-ff-033.wav",
                103: "39182__jobro__piano-ff-035.wav",
                
                #Flex Sensor connected to dreamer nano 
                112: "39172__jobro__piano-ff-025.wav",     #P
                111: "39174__jobro__piano-ff-027.wav",     #O
                105: "39176__jobro__piano-ff-029.wav",     #I
                117: "39178__jobro__piano-ff-031.wav",    # U
                121: "39180__jobro__piano-ff-033.wav",     #Y
                116: "39182__jobro__piano-ff-035.wav",     #T

                #force sensor on dreamer nano
                108: "39172__jobro__piano-ff-025.wav",     #     L
                107: "39176__jobro__piano-ff-029.wav",     #     K
                106: "39180__jobro__piano-ff-033.wav",     #     J
                104 : "39182__jobro__piano-ff-035.wav"     #    H
                }


#map tones to files for flex / force sensors
#generated at http://www.audiocheck.net/audiofrequencysignalgenerator_sinetone.php
tones = { 100: "audiocheck.net_sin_100Hz_-3dBFS_1s.wav",
          200: "audiocheck.net_sin_200Hz_-3dBFS_1s.wav",
          300: "audiocheck.net_sin_300Hz_-3dBFS_1s.wav",
          400: "audiocheck.net_sin_400Hz_-3dBFS_1s.wav",
          500: "audiocheck.net_sin_500Hz_-3dBFS_1s.wav"}



#map key numbers to GPIO pin for LED
leds =        { #arcade buttons on picade
                306: 20,
                308: 16,#24,
                32 : 12,
                304: 25,
                122: 24,#16,
                120: 23,
                #makey makey
                119: 21,
                97 : 5,
                115: 6,
                100: 13,
                102: 19,
                103: 26}

#HARDWARE SETUP
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

#flash all LEDS to check operation
for key, led in leds.items():
    print led
    GPIO.setup(led, GPIO.OUT) # LED pin set as output
    GPIO.output(led, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(led, GPIO.LOW)

#SET PORT FOR Flex / Force inputs
#See /Arduino folder for the code for this
sensor_port = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo_HIDPC-if00'
baud = 9600
sensors = serial.Serial(sensor_port, baud, timeout = 0)




#sound samples
SAMPLE_FOLDER = "samples"
TONE_FOLDER = "samples/tones"

#load samples
BANK = os.path.join(os.path.dirname(__file__), SAMPLE_FOLDER)
TONE_BANK = os.path.join(os.path.dirname(__file__), TONE_FOLDER)

#Set sound mixer up
pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)

#Create the dict to hold the references to the sound samples
samples = dict()
for key, sound in buttons.items():
    t= os.path.join(BANK, sound)
    s= pygame.mixer.Sound( t )
    samples[key] = s

#Create dict to hold refs to tone samples
toneSounds = dict()
for key, sound in tones.items():
    t= os.path.join(TONE_BANK, sound)
    s= pygame.mixer.Sound( t )
    toneSounds[key] = s

#tone variables
lasttone=100
tone=100 

#recording variables
recording = False
recordings = OrderedDict([(0,0)])
recordingLast = 0
RECORDINGS_FOLDER = "www/recordings"
RECORDINGS = os.path.join(os.path.dirname(__file__), RECORDINGS_FOLDER)

#playback
playing=False

def main():
    global tone
    global lasttone
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Pygame Keyboard Test')
    

    while True:
        #process pygame event queue
        for event in pygame.event.get():
            if (event.type == KEYUP):
                keyuphandler(event.key)
                
            if (event.type == KEYDOWN):
                keydownhandler(event.key)
            #if (event.type == PLAYSAMPLE):
            #    samples[event.sample].play(loops=0)

        #read force and flex sensors on serial port
        input = sensors.readline()
        #clean up message
        input = input.replace('\n', '')
        input = input.replace('\r', '')
        if(input != ""):
                values = input.split("#")
                flex = int(values[0])
                force = values[1]
                #print flex
                #map flex to a sound
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

def keyuphandler(key):
    #turn led off
    lightoff(key)
    pass

def playbackHandler(zero, thero, sound):
    #load file
    #play it
    #create a new thread
    print "playback"

    if (len(recordings) > 1):
        print "playback from memory"

    else:
        print "playback from file"
        recordings.clear()
        latestRecording = sorted(os.listdir(RECORDINGS))[-1]
        t= os.path.join(RECORDINGS, latestRecording)
        for key, val in csv.reader(open(t)):
            recordings[float(key)] = int(val)
            
    previoussoundindex = 0
    #wrap this in a loop in the new thread while(playing)
    for millis, soundindex in recordings.iteritems():
        print millis
        time.sleep(millis)

        #turn previous light off and current light on 
        lightoff(previoussoundindex)
        lighton(soundindex)
        previoussoundindex=soundindex
        
        if (sound):
            samples[soundindex].play(loops=0)

        #IF ITS THE LAST ONE MAKE SURE WE TURN THE LIGHT OFF
        if (soundindex == recordings[recordings.keys()[-1]]):
            #print "last irem"
            time.sleep(0.4)
            lightoff(soundindex)


        
        

    

def recordButtonHandler():
    global recording
    #handle start and stop recording

    if (recording):
        stopRecording()
        recording=False
    else:
        startRecording()
        recording=True
        
def startRecording():
    #empty array
    print "recording start"
    global recordings, recordingLast
    recordings.clear()
    recordingLast = time.time()

def stopRecording():
    #write out to file
    print "recording stop"
    print recordings
    timenow = time.time()
    filename = str(timenow) + ".csv"
    print filename
    t= os.path.join(RECORDINGS, filename)
    w = csv.writer(open(t, "w"))
    #w.writerow(["milliseconds", "keyindex"])
    for key, val in recordings.items():
        w.writerow([key, val])
    pass
    

    

def recordSound(soundindex):
    #record sound and timestamp to array or file
    global recordingLast
    timenow = time.time() 
    millis = timenow - recordingLast
    recordingLast = timenow
    print millis
    print recordingLast
    recordings[millis] = soundindex
    
def keydownhandler(key):
    #handle key presses
    global recording
    #turn led on
    print key
    
    #soundindex = key

    if (key == RECORD):
        recordButtonHandler()
    elif (key == PLAY):
        playbackHandler(0,0,True)
    elif (key == PLAY_NO_LIGHT):
        playbackHandler(0,0,False)
        
    #must be a sound key then!    
    else:
        
        if samples.has_key(key):
            samples[key].play(loops=0)
            lighton(key)
        else:
            print "not set"
        if (recording):
            recordSound(key)
    
def lighton(key):
    print "gpio"
    if leds.has_key(key):
        print leds[key]
        GPIO.output(leds[key], GPIO.HIGH)

def lightoff(key):
    if leds.has_key(key):
        GPIO.output(leds[key], GPIO.LOW)
    
    
main()
