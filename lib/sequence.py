#!/usr/bin/python3

import json
import subprocess
import glob
import os
import psutil

class Sequence:
    _quiet = True
    _bps = 120  # bps
    _repeat = False
    _transpose = 0
    _player = None
    _ppqn = 64
    _end = False
    

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.getPlayerInfo()

    def getPlayerInfo(self):
        with open("player.json","r") as player_file:
            playerInfo = json.load(player_file)
            self._bps= playerInfo["bps"]
            self._ppqn = playerInfo["ppqn"]
            self._repeat = playerInfo["repeat"]
            self._transpose = playerInfo["transpose"]  
            not self._quiet and print("getPlayerInfo:",playerInfo)

    def play(self):
        not self._quiet and print("play")
        self._player = subprocess.Popen(["python","player.py"])
        print("self._palyer",self._player)
        return{True}

    def writePlayerInfo(self):
        playerInfo = {}
        playerInfo["ppqn"] = self._ppqn
        playerInfo["bps"] = self._bps
        playerInfo["repeat"] = self._repeat
        playerInfo["transpose"] = self._transpose
        if self._end:
            playerInfo["end"] = self._end
        not self._quiet and print("writePlayerInfo:",playerInfo)
        with open("player.json","w") as player_file:
            json.dump(playerInfo, player_file)

    def getSequences(self):
        return glob.glob("sequences/*.abc")

    def getSequence(self,name):
        with open("sequences/" + name,"r") as sequence_file:
            return sequence_file.read()
        return False

    def writeSequence(self,name,sequence):
        with open("sequences/" + name,"w") as sequence_file:
            return sequence_file.write(sequence)
        return False

    def removeSequence(self,name):
        try:
            os.remove("./sequences/" + name)
            return True
        except:
            return False

    def isPlaying(self) :
        # Check if there are any running scripts
        for process in psutil.process_iter(['username','cmdline','pid']):
            if process.info["username"] == "pi":
                cmdline = process.info["cmdline"]
                if cmdline is not None:
                    if len(cmdline)>=2:
                        if cmdline[1] == "player.py":
                            return (True)
        return (False)


    # *********  Getters &  Setters  ********

   
    @property
    def ppqn(self): 
        return self._ppqn

    @ppqn.setter
    def bps(self, ppqn=64):
        self.getPlayerInfo()
        self._ppqn = ppqn
        self.writePlayerInfo()

    @property
    def bps(self): 
        return self._bps

    @bps.setter
    def bps(self, bps):
        self.getPlayerInfo()
        self._bps = bps
        self.writePlayerInfo()

    @property
    def repeat(self): 
        return self._repeat

    @repeat.setter
    def repeat(self, repeat):
        self.getPlayerInfo()
        self._repeat = repeat
        self.writePlayerInfo()

    @property
    def transpose(self): 
        return self._transpose

    @transpose.setter
    def transpose(self, transpose):
        self.getPlayerInfo()
        self._transpose = transpose
        self.writePlayerInfo()

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self.getPlayerInfo()
        self._end = end
        self.writePlayerInfo()



