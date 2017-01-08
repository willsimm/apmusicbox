import pygame, time
from pygame.locals import *
import os
import glob
import csv
from collections import OrderedDict
from threading import Thread


#sound to headphone not hdmi
#amixer cset numid=3 2
#sounds from https://www.freesound.org/people/jobro/packs/2489/

#array sounds:keys
sounds = { 256 : 265}

#function buttons
RECORD = 257 # KEY 1
PLAY = 258 # KEY 2



#array leds:keys

#sound samples
SAMPLE_FOLDER = "samples"

#load samples

BANK = os.path.join(os.path.dirname(__file__), SAMPLE_FOLDER)

pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)

files = glob.glob(os.path.join(BANK, "*.wav"))
files.sort()

samples = [pygame.mixer.Sound(f) for f in files]


#recording variables
recording = False
recordings = OrderedDict([(0,0)])
recordingLast = 0
RECORDING_FOLDER = "recordings"

#playback
PLAYSAMPLE = USEREVENT+1

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Pygame Keyboard Test')
    

    while True:

        for event in pygame.event.get():
            if (event.type == KEYUP):
                keyuphandler(event.key)
                
            if (event.type == KEYDOWN):
                keydownhandler(event.key)
            if (event.type == PLAYSAMPLE):
                samples[event.sample].play(loops=0)

def keyuphandler(key):
    #turn led off
    pass

def playbackHandler():
    #load file
    #play it
    #create a new thread
    print "playback"
    for millis, soundindex in recordings.iteritems():
        print millis
        time.sleep(millis)
        samples[soundindex].play(loops=0)

        # creating the event
        #my_event = pygame.event.Event(PLAYSAMPLE, sample=soundindex)
        #pygame.event.post(my_event)

        
        

    

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
    global recordings, recordingLast
    recordings.clear()
    recordingLast = time.time()

def stopRecording():
    #write out to file

    print recordings
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
    
    soundindex = key-96

    if (key == RECORD):
        recordButtonHandler()
    elif (key == PLAY):
        t = Thread(target=playbackhandler)
        t.daemon = True
        t.start()
        #playbackHandler()
        
    #must be a sound key then!    
    else:        
        if (soundindex > 0 and soundindex < len(samples)) :
            samples[soundindex].play(loops=0)
        if (recording):
            recordSound(soundindex)

    

    


main()
