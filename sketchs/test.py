#!/usr/bin/python3



from abcHelper import AbcHelper

o = AbcHelper("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
for seq in o.sequence:
    print(seq["ppqn"],seq["actions"])
