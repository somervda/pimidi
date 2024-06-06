#! /usr/bin/python3

#Timers
#Excute code at timed intervals

import time
import json
import gc
from threading import Timer
from abcHelper import AbcHelper
from midiio import MidiIO

import argparse




_bps=80
_repeat = False
_cycle= 0
_transpose = 0
_pendingTranspose = 0
_onNote = 0
_end = False
# Pulses per quarter note
_ppqn=32
_abcFileName = ""
_abc=""
_ppqnSequenceIndex=0

midiio = MidiIO()

def doPPQN():
    # do actions to be performed on the current ppqn value
    # then read the next ppqn value and set the timer interval to the
    # interval until the next ppqn value
    global _bps
    global _transpose
    global _pendingTranspose
    global _end


    global tPPQN
    global tComm
    global _ppqn
    global _ppqnSequenceIndex
    nstart =0
    # print(tPPQN.interval,abchelper.sequence[_ppqnSequenceIndex]['actions'],time.time(),_ppqnSequenceIndex,_bps,len(abchelper.sequence),_transpose)
    # Note: midiio.noteon and notoff take some time so ajust timing based on the overhead , also turn of note display setting on pymidi
    # device, it slows down the note playing
    for action in abchelper.sequence[_ppqnSequenceIndex]['actions']:
        match action["action"]:
            case "on":
                if not _end:
                    nstart = time.time()
                    midiio.noteOn(action["note"] + _transpose)
            case "off":
                midiio.noteOff(action["note"] + _transpose)
                # print("_end:",_end)
                if _end:
                    tPPQN.cancel() 
                    tComm.cancel()
    _ppqnSequenceIndex+=1
    # Calculate the difference between ppqn values
    if _ppqnSequenceIndex < len(abchelper.sequence) :
        ppqnDelta = abchelper.sequence[_ppqnSequenceIndex]['ppqn'] - abchelper.sequence[_ppqnSequenceIndex-1]['ppqn']
        interval = (60 * ppqnDelta)/(_bps * _ppqn)  - (time.time() - nstart )
        if interval > 0 :
            tPPQN.interval=interval
        else:
            tPPQN.interval=0.001
        # print(abchelper.sequence[_ppqnSequenceIndex]['ppqn'] ,ppqnDelta,(60 * ppqnDelta)/(_bps * _ppqn))
    else:
        # print(len(abchelper.sequence),_ppqnSequenceIndex)
        tPPQN.cancel() 
        tComm.cancel()



def updateComm():
    getComm()




# def writeComm(beat):
#     # write an updated comm.json file
#     with open("comm.json","w") as comm_file:
#         comm={}
#         comm["beat"]=beat
#         comm_file.write(json.dumps(comm))


#Interval timer
#Wrap it into a class
#Make it run until we stop it
#Notice we can have multiple timers at once!
#https://docs.python.org/3/library/threading.html#threading.Thread.run

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
        # print('Done')
    
def getComm():
    global _bps
    global _ppqn
    global _repeat
    global _pendingTranspose
    global _onNote
    global _end
    global _abcFileName
    # Get playing info
    # This seems pretty quick (about 500 milliseconds when I measured it)
    # Note: When transpossing it makes sure any playing note is turned of first (Midi leaves it playing otherwise)

    try:
        with open("player.json","r") as comm_file:
            comm = json.load(comm_file)
            _abcFileName = "sequences/" + comm["sequence"]
            _bps= comm["bps"]
            _ppqn = comm["ppqn"]
            _repeat = comm["repeat"]
            # Transpose only done on start of a cycle
            _pendingTranspose = comm["transpose"]  
            _end = comm["end"]
            # print("Comm:",_bps,_repeat,_transpose,_end)
    except:
        pass

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='Play a sequence of abc notation notes')
    # parser.add_argument('--file', dest='abcFile', help='abc notation file containing sequence to played',required=True,type=argparse.FileType('r'))
    # parser.add_argument('--ppqn', dest='ppqn', type=int, help='Parts per quarter note (ppqn) value used for quantizing the sequence timing', required=False, default=16)
    # args = parser.parse_args()
    # _ppqn=args.ppqn
    gc.disable()

    # *** Watch out for **** - displaying notes values on the pimidi device slows things down , turn this setting off 
    #  when using the sequencer
    midi_display_setting = midiio.midi_display
    midiio.midi_display = False

    getComm()
    with open( _abcFileName,"r") as abcfile:
        _abc=abcfile.read()
    abchelper=AbcHelper(_abc,_ppqn)
    # print(_abcFileName,_ppqn,_bps,_abc,abchelper.sequence)

    # print(abchelper.sequence)
    #Really we are making a thread and controlling it
    # tPPQN is invoked every ppqn action in the abchelper.sequence
    # do the first ppqn action at the first ppqn value in the sequence (Then adjust as we go on)
    while (_cycle==0 or _repeat) and (not _end):
        _transpose = _pendingTranspose
        _ppqnSequenceIndex = 0
        firstPPQNInterval = abchelper.sequence[_ppqnSequenceIndex]['ppqn'] * (60/(_bps*_ppqn))
        # print(firstPPQNInterval)
        tPPQN = RepeatTimer(firstPPQNInterval,doPPQN)
        # tComm runs periodically to get any new communication and apply it
        tComm = RepeatTimer(.1,updateComm)
        # print('threading started')
        tPPQN.start() 
        tComm.start()

        while not tPPQN.finished.is_set():
            time.sleep(.01)

            
        _cycle += 1
        # print('threading finished')

    midiio.midi_display = midi_display_setting


