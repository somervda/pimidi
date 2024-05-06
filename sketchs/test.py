#!/usr/bin/python3
import sys


from abc import ABC

o = ABC("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
for seq in o.sequence:
    print(seq["ppqn"],seq["actions"])