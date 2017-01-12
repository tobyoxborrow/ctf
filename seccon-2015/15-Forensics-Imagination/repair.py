#!/usr/bin/env python

import argparse
import bitstring
import sys


# png format reference:
# http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

DATA = None
POS = 0
VERBOSE = 0


def load_data_file(filename):
    global DATA
    if VERBOSE:
        print('filename: %s' % filename)
    f = open(filename, 'rb')
    DATA = f.read()
    f.close()
    return True


def read_file_magic():
    global POS

    if DATA[0:8] == '\x89\x0d\x0a\x1a\x0a\x00\x00\x00':
        POS = 1 * 8
        if VERBOSE:
            print('Repairing file magic')

    elif DATA[0:4] == '\x89\x50\x4e\x47':
        POS = 4 * 8
        if VERBOSE:
            print('File magic: PNG')

    else:
        print('Did not find PNG file magic')
        print('Can not handle this file type')
        sys.exit(-1)

    return '\x89\x50\x4e\x47'


def read_bitsream(length):
    global POS
    bs = bitstring.BitStream(bytes=DATA, length=length, offset=POS)
    POS += length
    return bs


def main():
    global VERBOSE

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--filename', '-f',
                        default='41221d6d81c5df683c1041a1af07d25d')
    args = parser.parse_args()

    VERBOSE = args.verbose

    load_data_file(args.filename)

    file_magic = read_file_magic()

    new_bit_stream = bitstring.pack('bytes:4, bytes',
                                    file_magic,
                                    DATA[int(POS / 8):])

    f = open('41221d6d81c5df683c1041a1af07d25d.png', 'wb')
    f.write(''.join(new_bit_stream.unpack('bytes')))
    f.close()


main()
