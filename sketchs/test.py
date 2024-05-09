#!/usr/bin/python3



from abcHelper import AbcHelper

o = AbcHelper("|: A | d/2A/F2 DFz | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|",24)
# for seq in o.sequence:
#     print(seq["ppqn"],seq["actions"])
print(o.sequence)
    
