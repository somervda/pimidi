#!/usr/bin/python3

import json
import subprocess
import glob
import os
import psutil

class Sequence:
    _quiet = True
    _bpm = 120  # bpm
    _repeat = False
    _transpose = 0
    _player = None
    _ppqn = 64
    _end = False
    # Default abc notation used by the player
    _abcDefault = ""
    

    def __init__(self,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self.getPlayerInfo()

    def getPlayerInfo(self):
        with open("player.json","r") as player_file:
            playerInfo = json.load(player_file)
            self._bpm= playerInfo["bpm"]
            self._ppqn = playerInfo["ppqn"]
            self._repeat = playerInfo["repeat"]
            self._transpose = playerInfo["transpose"]  
            not self._quiet and print("getPlayerInfo:",playerInfo)

    def play(self):
        self._player = subprocess.Popen(["python","player.py"])
        return (True)

    def writePlayerInfo(self):
        playerInfo = {}
        playerInfo["ppqn"] = self._ppqn
        playerInfo["bpm"] = self._bpm
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
                            # print("process:",process)
                            return (True)
        return (False)


    # *********  Getters &  Setters  ********

    @property
    def abcDefault(self): 
        return self._abcDefault
   
    @abcDefault.setter
    def abcDefault(self, abcDefault=""):
        self._abcDefault = abcDefault
        with open("sequences/default.abc" ,"w") as sequence_file:
            return sequence_file.write(self._abcDefault)


    @property
    def ppqn(self): 
        return self._ppqn


    @ppqn.setter
    def bpm(self, ppqn=64):
        self.getPlayerInfo()
        self._ppqn = ppqn
        self.writePlayerInfo()

    @property
    def bpm(self): 
        return self._bpm

    @bpm.setter
    def bpm(self, bpm):
        self.getPlayerInfo()
        self._bpm = bpm
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
        # Special for end logic, write out end to player.json
        # but reset _end value after that
        self._end = False



