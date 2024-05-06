#!/usr/bin/python3

from abc import ABC

o = ABC("|: A | dAF DFA | ded cBA | dcd efg | fdf ecA | dAF DFA | ded cBA | dcd efg fdd d2 :|")
print(o.PPQN.get("95",{}))
print(o.PPQN.get("96",{}))