import pygame, time
from pygame.locals import *
import os
import glob

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
recordingStart = 0
RECORDING_FOLDER = "recordings"


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

def keyuphandler(key):
    #turn led off
    pass

def playback():
    print "playback"
    
def keydownhandler(key):
    global recording
    #turn led on
    print key
    if (key == RECORD):
        recording = not recording
        print recording
    elif (key == PLAY):
        playback()
    else:        
        soundindex = key-96
        if (soundindex > 0 and soundindex < len(samples)) :
            samples[soundindex].play(loops=0)
    

    


main()
