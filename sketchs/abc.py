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

class AbcHelper:
    _abc = ""
    _sequence = []
    _quiet = True

    def __init__(self,abc,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._abc=abc
        self.toSequence()


    def toSequence(self):
        # Convert the abc notation to a sequence
        # Read each character until start is found
        hasStarted = False
        semiToneAdjust=0
        midi=0
        noteDuration = 4
        for abcChar in self._abc:
            # Skip over bar and blank space
            if abcChar not in ["|"," "] :
                match abcChar:
                    case "^":
                        # sharp
                        semiToneAdjust-=1
                    case "_":
                        # flat
                        semiToneAdjust-=1
                    case "=":
                        # natural (Not supported yet)
                        semiToneAdjust=0
                    case "C":
                        midi=60
                        hasStarted = True
                    case "D":
                        midi=62
                        hasStarted = True
                    case "E":
                        midi=64
                        hasStarted = True
                    case "F":
                        midi=65
                        hasStarted = True
                    case "G":
                        midi=67
                        hasStarted = True
                    case "A":
                        midi=69
                        hasStarted = True
                    case "B":
                        midi=71
                        hasStarted = True
                    case "c":
                        midi=72
                        hasStarted = True
                    case "d":
                        midi=74
                        hasStarted = True
                    case "e":
                        midi=76
                        hasStarted = True
                    case "f":
                        midi=77
                        hasStarted = True
                    case "g":
                        midi=79
                        hasStarted = True
                    case "a":
                        midi=81
                        hasStarted = True
                    case "b":
                        midi=83
                        hasStarted = True
                    case "\'":
                        midi += 12
                    case ",":
                        midi -= 12
                    case "/":
                        midi -= 12









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

# o = ABC("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
# for seq in o.sequence:
#     print(seq["ppqn"],seq["actions"])
# print(o.sequence)
