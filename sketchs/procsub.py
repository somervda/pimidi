#! /usr/bin/python3

#Timers
#Excute code at timed intervals

import time
import json
from threading import Timer
from abcHelper import AbcHelper
from midiio import MidiIO

import argparse




_bps=60
# Pulses per quarter note
_ppqn=32
_abc=""
_ppqnSequenceIndex=0

midoio = MidiIO()

def doPPQN():
    # do actions to be performed on the current ppqn value
    # then read the next ppqn value and set the timer interval to the
    # interval until the next ppqn value
    global _bps
    global tPPQN
    global _ppqn
    global _ppqnSequenceIndex
    print(tPPQN.interval,abchelper.sequence[_ppqnSequenceIndex]['actions'],time.time())
    for action in abchelper.sequence[_ppqnSequenceIndex]['actions']:
        match action.action:
            case "on":
                midoio.noteOn(action.note)
            case "off":
                midoio.noteOff(action.note)
    _ppqnSequenceIndex+=1
    # Calculate the difference between ppqn values
    ppqnDelta = abchelper.sequence[_ppqnSequenceIndex]['ppqn'] - abchelper.sequence[_ppqnSequenceIndex-1]['ppqn']
    tPPQN.interval=(60 * ppqnDelta)/(_bps * _ppqn)

def getComm():
    global _bps
    try:
        # Read the comm.json file to get 
        # any new data
        with open("data.json","r") as comm_file:
            comm = json.load(comm_file)
            _bps= comm["bps"]
    except:
        pass


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
        print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Play a sequence of abc notation notes')
    parser.add_argument('--file', dest='abcFile', help='abc notation file containing sequence to played',required=True,type=argparse.FileType('r'))
    parser.add_argument('--ppqn', dest='ppqn', type=int, help='Parts per quarter note (ppqn) value used for quantizing the sequence timing', required=False, default=16)
    args = parser.parse_args()
    _ppqn=args.ppqn
    with args.abcFile as abcfile:
        _abc=abcfile.read()
    abchelper=AbcHelper(_abc,_ppqn)
    # print(abchelper.sequence)
    #Really we are making a thread and controlling it
    # tPPQN is invoked every ppqn action in the abchelper.sequence
    # do the first ppqn action at the first ppqn value in the sequence (Then adjust as we go on)
    firstPPQNInterval = abchelper.sequence[_ppqnSequenceIndex]['ppqn'] * (60/(_bps*_ppqn))
    print(firstPPQNInterval)
    tPPQN = RepeatTimer(firstPPQNInterval,doPPQN)
    # tComm runns periodically to get any new communication and apply it
    tComm = RepeatTimer(1,getComm)
    print('threading started')
    tPPQN.start() 
    tComm.start()

    while True:
        time.sleep(1)
        
    print('threading finishing')

    tPPQN.cancel()
    tComm.cancel()
