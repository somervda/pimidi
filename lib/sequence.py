#!/usr/bin/python3

import json

class Sequence:
    _quiet = True
    _sequenceFile = ""
    _bps = 120  # bps
    _repeat = False
    _transpose = 0
    _player = None
    

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")

    def play(self):
        self._player = subprocess.Popen(["python","player.py","--file","sequences/" + self._sequenceFile])
        return{True}

    def writePlayerInfo(self):
        playerInfo = {}
        playerInfo["sequence"] = self._sequenceFile
        playerInfo["bps"] = self._bps
        playerInfo["repeat"] = self._repeat
        playerInfo["transpose"] = self._transpose
        with open("player.json","w") as player_file:
            json.dump(playerInfo, player_file)

    # *********  Getters &  Setters  ********

    @property
    def file(self): 
        print ('called getter')
        return self._sequenceFile

    @file.setter
    def file(self,sequenceFile):
        self._sequenceFile = sequenceFile
        self.writePlayerInfo()
    
    # @bps.setter
    # def bps(self, bps):
    #     self._bps = bps
    #     self.writePlayerInfo()

    # @repeat.setter
    # def repeat(self, repeat):
    #     self._repeat = repeat
    #     self.writePlayerInfo()

    # @transpose.setter
    # def transpose(self, transpose):
    #     self._transpose = transpose
    #     self.writePlayerInfo()



