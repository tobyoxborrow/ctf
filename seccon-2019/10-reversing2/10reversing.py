#!/usr/bin/env python3

import sys

from collections import defaultdict


def crack_key(o, i):
    """
    Try all possible keyfile values (ascii 0x1 to 0x7e) for a given input
    character (i) until we find one that matches the outfile character (o)
    """
    o1 = ord(o)     # outfile char
    for k in range(0x1, 0x7e):     # possible keyfile values
        x = o1 ^ 0x80
        x = x - k
        if x >= 0x1 and x <= 0x7e:
            if chr(x) == i:
                return chr(k)
        x = o1 - k
        if x >= 0x1 and x <= 0x7e:
            if chr(x) == i:
                return chr(k)

    return None


def decrypt_char(o, k):
    """
    Decrypt a single outfile character using a single keyfile character
    """
    o1 = ord(o)     # outfile char
    k1 = ord(k)     # keyfile char

    x = o1 ^ 0x80
    x = x - k1
    if x >= 0x1 and x <= 0x7e:
        return chr(x)

    x = o1 - k1
    if x >= 0x1 and x <= 0x7e:
        return chr(x)

    return None


def decrypt(outfile, keyfile):
    """
    Decrypt the outfile string using a given keyfile string
    """
    decrypted = ""
    for index, o in enumerate(outfile):
        mod = index % 7
        k = keyfile[mod]
        d = decrypt_char(o, k)
        d_ord = ord(d)
        d_hex = hex(d_ord)
        o_repr = repr(o)
        print(f"{index:2d} {mod:2d} {o_repr: >7s} {k: >2s} {d: >2s} {d_ord:3d} {d_hex: >5s}")
        decrypted += d
    return decrypted


def main():
    """
    Decrypt an outfile
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "outfile"

    outfile = ""
    with open(filename, 'r') as hdl:
        outfile = hdl.readline()

    keyfile = defaultdict(str)

    # some chunk chars we assume we know some possible inputs
    keyfile[0] = crack_key(outfile[0], "f")
    keyfile[1] = crack_key(outfile[1], "l")
    keyfile[2] = crack_key(outfile[2], "a")
    keyfile[3] = crack_key(outfile[3], "g")
    keyfile[4] = crack_key(outfile[4], "{")
    keyfile[5] = crack_key(outfile[5], "T")
    keyfile[6] = crack_key(outfile[6], "e")

    keyfile_str = ""
    for i in range(0, 7):
        if i in keyfile:
            keyfile_str += keyfile[i]
        else:
            keyfile_str += "_"

    decrypted = decrypt(outfile, keyfile_str)

    positions = ''.join(str(i) for i in range(0, 7)) * 9
    print(f"keyfile:    {keyfile_str}")
    print(f"            {positions}")
    print(f"plain-text: {decrypted}")
    print(f"outfile:    {outfile}")


if __name__ == '__main__':
    main()
