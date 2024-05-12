#!/usr/bin/python3



from abcHelper import AbcHelper

o = AbcHelper('|: "A" z/2| "Dm" d/2A/F2 "D7" DFz | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|',24)
# for seq in o.sequence:
#     print(seq["ppqn"],seq["actions"])
print(o.sequence)
    
