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

    _hasStarted = False
    _semiToneAdjust=0
    _midi=0
    _noteDuration = 1
    # _pendingAction is a noteOff at next ppqn time
    _PendingAction={}

    _ppqn=24
    _ppqnNumber=0

    def __init__(self,abc,ppqn,quiet=True):
        self._quiet = quiet
        not self._quiet and print("__init__")
        self._abc=abc
        self._ppqn=ppqn
        # self.toSequence()
        self.addSequence(24)


    def toSequence(self):
        # Convert the abc notation to a sequence
        # Read each character until start is found
        

        for abcChar in self._abc:
            # Skip over bar and blank space
            if abcChar not in ["|"," "] :
                match abcChar:
                    case "^":
                        # sharp
                        self._semiToneAdjust-=1
                    case "_":
                        # flat
                        self._semiToneAdjust-=1
                    case "=":
                        # natural (Not supported yet)
                        self._semiToneAdjust=0
                    case "C":
                        self._midi=60
                        self._hasStarted = True
                    case "D":
                        self._midi=62
                        self._hasStarted = True
                    case "E":
                        self._midi=64
                        self._hasStarted = True
                    case "F":
                        self._midi=65
                        self._hasStarted = True
                    case "G":
                        self._midi=67
                        self._hasStarted = True
                    case "A":
                        self._midi=69
                        self._hasStarted = True
                    case "B":
                        self._midi=71
                        self._hasStarted = True
                    case "c":
                        self._midi=72
                        self._hasStarted = True
                    case "d":
                        self._midi=74
                        self._hasStarted = True
                    case "e":
                        self._midi=76
                        self._hasStarted = True
                    case "f":
                        self._midi=77
                        self._hasStarted = True
                    case "g":
                        self._midi=79
                        self._hasStarted = True
                    case "a":
                        self._midi=81
                        self._hasStarted = True
                    case "b":
                        self._midi=83
                        self._hasStarted = True
                    case "\'":
                        self._midi += 12
                    case ",":
                        self._midi -= 12
                    case "/":
                        self._noteDuration /= 2


    def checkForNoteWrite(self):
        # performed when we see a new note being defined in the abc notation
        if self._hasStarted:
            # Newnote info so write out last one
            midi += self._semiToneAdjust
            if self._PendingAction == []:
                # No pending action to write so just write out midi note
                self.addSequence([{"note":self._midi,"action":"on"}])
            else:    
                self.addSequence([ self._pendingAction,{"note":self._midi,"action":"on"}])
            self._ppqnNumber+= self._ppqn * self._noteDuration
            # Resetup for next note
            self._hasStarted=False
            self._midi=0
            self._semiToneAdjust=0
            self._PendingAction=[]
            self._noteDuration=1







    def addSequence(self,actions):
        self._sequence.append({"ppqn":self._ppqn,"actions":actions})





    # getters

    def getSequence(self):
        not self._quiet and print("getSequence")
        return self._sequence
    sequence = property(getSequence)

# o = ABC("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
# for seq in o.sequence:
#     print(seq["ppqn"],seq["actions"])
# print(o.sequence)
