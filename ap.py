#tasks
#led to each GPIO 1-12
#keymap
#custom inputs - linked to one dreamer nano
#save to file
#load from file
#webserver to edit file



#map key to sound
# map key to function





import pygame, time
from pygame.locals import *
import os
import glob
import csv
from collections import OrderedDict
#from threading import Thread
import thread

#sound to headphone not hdmi
#amixer cset numid=3 1 (2 for hdmi, 0 for auto)
#sounds from https://www.freesound.org/people/jobro/packs/2489/

#array sounds:keys
sounds = { 256 : 265}

#function buttons
RECORD = 257 # KEY 1
PLAY = 258 # KEY 2



#array leds:keys

kb = True

if(kb):
    buttons = {113: "000_base.wav",
        119: "001_cowbell.wav",
        101 : "002_clash.wav",
        114: "003_whistle.wav",
        116: "004_rim.wav",
        121: "005_hat.wav",
        97: "39172__jobro__piano-ff-025.wav",
        115: "39174__jobro__piano-ff-027.wav",
        100 : "39176__jobro__piano-ff-029.wav",
        102: "39178__jobro__piano-ff-031.wav",
        103: "39180__jobro__piano-ff-033.wav",
        104: "39182__jobro__piano-ff-035.wav"}
else:
    buttons = {306: "000_base.wav",
        308: "001_cowbell.wav",
        32 : "002_clash.wav",
        304: "003_whistle.wav",
        122: "004_rim.wav",
        120: "005_hat.wav",
        119: "39172__jobro__piano-ff-025.wav",
        97: "39174__jobro__piano-ff-027.wav",
        115 : "39176__jobro__piano-ff-029.wav",
        100: "39178__jobro__piano-ff-031.wav",
        102: "39180__jobro__piano-ff-033.wav",
        103: "39182__jobro__piano-ff-035.wav"}


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

#sound samples
SAMPLE_FOLDER = "samples"

#load samples

BANK = os.path.join(os.path.dirname(__file__), SAMPLE_FOLDER)

pygame.mixer.init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(16)


files = list()
for key, sound in buttons.items():
    files.append( {key: glob.glob(os.path.join(BANK, sound))} )

print files


files = glob.glob(os.path.join(BANK, "*.wav"))
files.sort()

for f in files:
    print f

samples = [pygame.mixer.Sound(f) for f in files]


#recording variables
recording = False
recordings = OrderedDict([(0,0)])
recordingLast = 0
RECORDING_FOLDER = "recordings"

#playback
#PLAYSAMPLE = USEREVENT+1
playing=False

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
            #if (event.type == PLAYSAMPLE):
            #    samples[event.sample].play(loops=0)

def keyuphandler(key):
    #turn led off
    pass

def playbackHandler(zero, thero):
    #load file
    #play it
    #create a new thread
    print "playback"
    #global playing

    #if (playing):
    #    playing=False
    #else:
    #    playing=True

    #wrap this in a loop in the new thread while(playing)
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
        #t = Thread(target=self.playbackhandler)
        #t.daemon = True
        #t.start()
        #thread.start_new_thread(playbackHandler, (0,0))
        playbackHandler(0,0)
        
    #must be a sound key then!    
    else:        
        if (soundindex > 0 and soundindex < len(samples)) :
            samples[soundindex].play(loops=0)
        if (recording):
            recordSound(soundindex)

    

    


main()
