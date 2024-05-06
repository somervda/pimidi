#!/usr/bin/python3

# load an abc notation  and convert it to 
# my PPQN data
# sequence is an array of arrays  
# with one entry per PPQN value, the entry is an array of actions for that PPQN value eg:
# [
#  {'ppqn': 60, 'actions': [{'note': 62, 'action': 'on'}, {'note': 65, 'action': 'off'}]},
#  {'ppqn': 120, 'actions': [{'note': 62, 'action': 'on'}, {'note': 65, 'action': 'off'}]}, 
#  {'ppqn': 240, 'actions': [{'note': 62, 'action': 'on'}, {'note': 65, 'action': 'off'}]}
# ]

class ABC:
    _abc = ""
    _sequence = []
    _quiet = True

    def __init__(self,abc,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._abc=abc
        self.addSequence(60)
        self.addSequence(120)
        self.addSequence(240)

    def addSequence(self,ppqn):
        actions=[]
        actions.append({"note":62,"action":"on"})
        actions.append({"note":65,"action":"off"})
        self._sequence.append({"ppqn":ppqn,"actions":actions})




    # getters

    def getSequence(self):
        not self._quiet and print("getSequence")
        return self._sequence
    sequence = property(getSequence)

o = ABC("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
for seq in o.sequence:
    print(seq["ppqn"],seq["actions"])
print(o.sequence)
