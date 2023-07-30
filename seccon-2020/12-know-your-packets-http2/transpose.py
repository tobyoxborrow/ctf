#!/usr/bin/env python
"""
Transpose two pairs of characters with each other.
So abcd becomes badc
"""

CHARS = ""

with open('hex_output', 'r') as hdl:
    for line in hdl.readlines():
        for char in line:
            CHARS += char

print(CHARS)

HCRSA = ""

for index in range(0, len(CHARS), 2):
    a = CHARS[index]
    b = CHARS[index+1]

    HCRSA += b + a

print(HCRSA)
