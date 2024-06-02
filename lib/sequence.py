#!/usr/bin/python3

import json
import subprocess

class Sequence:
    _quiet = True
    _sequenceFile = ""
    _bps = 120  # bps
    _repeat = False
    _transpose = 0
    _player = None
    _ppqn = 64
    

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")

    def play(self):
        not self._quiet and print("play")
        self._player = subprocess.Popen(["python","player.py"])
        return{True}

    def writePlayerInfo(self):
        playerInfo = {}
        playerInfo["sequence"] = self._sequenceFile
        playerInfo["ppqn"] = self._ppqn
        playerInfo["bps"] = self._bps
        playerInfo["repeat"] = self._repeat
        playerInfo["transpose"] = self._transpose
        not self._quiet and print("writePlayerInfo:",playerInfo)
        with open("player.json","w") as player_file:
            json.dump(playerInfo, player_file)

    # *********  Getters &  Setters  ********

    @property
    def sequenceFile(self): 
        return self._sequenceFile

    @sequenceFile.setter
    def sequenceFile(self,file):
        self._sequenceFile = file
        self.writePlayerInfo()
    
    @property
    def ppqn(self): 
        return self._ppqn

    @ppqn.setter
    def bps(self, ppqn=64):
        self._ppqn = ppqn
        self.writePlayerInfo()

    @property
    def bps(self): 
        return self._bps

    @bps.setter
    def bps(self, bps):
        self._bps = bps
        self.writePlayerInfo()

    @property
    def repeat(self): 
        return self._repeat

    @repeat.setter
    def repeat(self, repeat):
        self._repeat = repeat
        self.writePlayerInfo()

    @property
    def transpose(self): 
        return self._transpose

    @transpose.setter
    def transpose(self, transpose):
        self._transpose = transpose
        self.writePlayerInfo()



