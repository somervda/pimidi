#!/usr/bin/python3

# load an abc notation  and convert it to 
# my PPQN data
# PPQN is a dictionary  {"<ppqnseq>":[{"note":123,"action":"on"},{"note":120,"action":"off"}]}
# with one entry per ppqn sequence number, the entry is an array of actions
# action ={"note":<midi note value>,"action":"on|off"}

class ABC:
    _abc = ""
    _PPQN = {}
    _quiet = True
    def __init__(self,abc,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._abc=abc
        self.buildPPQN()

    def buildPPQN(self):
        actions=[]
        actions.append({"note":62,"action":"on"})
        self._PPQN["96"] = actions




    # getters

    def getPPQN(self):
        not self._quiet and print("getPPQN")
        return self._PPQN
    PPQN = property(getPPQN)

    
