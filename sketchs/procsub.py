#! /usr/bin/python3

#Timers
#Excute code at timed intervals

import time
import json
from threading import Timer
from abcHelper import AbcHelper

_bps=280
# Pulses per quarter note
_ppqn=32


def doBeat():
    global _bps
    global tBeat
    global _ppqn
    tBeat.interval=60/(_bps * _ppqn)
    print(time.time(),_bps,tBeat.interval)

def getComm():
    global _bps
    try:
        # Read the comm.json file to get 
        # any new data
        with open("data.json","r") as comm_file:
            comm = json.load(comm_file)
            _bps= comm["bps"]
            print("beat",_bps)
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

#Really we are making a thread and controlling it
# tBeat is invoked every beet to do what is needed on that beat
tBeat = RepeatTimer(.5,doBeat)
# tComm runns periodically to get any new communication and apply it
tComm = RepeatTimer(1,getComm)
print('threading started')
tBeat.start() 
tComm.start()

while True:
    time.sleep(1)
    
print('threading finishing')

tBeat.cancel()
tComm.cancel()
