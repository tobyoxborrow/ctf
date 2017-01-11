#!/usr/bin/env python

from __future__ import print_function

import argparse
import bitstring
import sys

# flac format reference:
# https://xiph.org/flac/format.html#metadata_block_streaminfo

DATA = None
POS = 0
VERBOSE = 1


def load_data_file(filename):
    '''Read binary data file'''
    global DATA
    if VERBOSE:
        print('filename: %s' % filename)
    f = open(filename, 'rb')
    DATA = f.read()
    f.close()
    return True


def read_file_magic():
    '''Read the file magic from the data file'''
    global POS

    # skip over the magic REDACTED starting point of the file
    if DATA[0:8] == 'REDACTED':
        POS = 8 * 8
        if VERBOSE:
            print('File magic: REDACTED')

    else:
        if DATA[0:4] == 'fLaC':
            POS = 4 * 8
            if VERBOSE:
                print('File magic: fLaC')

        else:
            print('Did not find fLaC stream marker')
            print('Can not handle this file type')
            sys.exit(-1)


def read_bitsream(length):
    '''Return a bitstream of x bits from the data file'''
    global POS
    bs = bitstring.BitStream(bytes=DATA, length=length, offset=POS)
    POS += length
    return bs


def generate_stream_marker():
    '''Return the correct flac stream marker for the data file'''
    return 'fLaC'


def read_metadata_blocks():
    '''Process the FLAC metadata blocks from the data in the bitstream'''
    global POS

    metadata_blocks = ''

    last_block = 0

    while not last_block:
        metadata_block_header = read_bitsream(32)
        last_block = metadata_block_header.read('bool')
        block_type = metadata_block_header.read('uint:7')
        block_length = metadata_block_header.read('uint:24')
        if VERBOSE:
            print('Metadata Block Header')
            print(' Bytes: %s' % metadata_block_header)
            block_type_friendly = ''
            if block_type == 0:
                block_type_friendly = ' (Stream Info)'
            elif block_type == 1:
                block_type_friendly = ' (Padding)'
            elif block_type == 3:
                block_type_friendly = ' (Seektable)'
            elif block_type == 4:
                block_type_friendly = ' (Vorbis Comment)'
            print(' Last flag: %s' % last_block)
            print(' Type: %s%s' % (block_type, block_type_friendly))
            print(' Length: %s' % block_length)

        # metadata block data
        if int(block_type) == 0:
            # STREAMINFO
            metadata_block = read_bitsream(block_length * 8)
            minimum_block_size = metadata_block.read('uint:16')
            maximum_block_size = metadata_block.read('uint:16')
            minimum_frame_size = metadata_block.read('uint:24')
            maximum_frame_size = metadata_block.read('uint:24')
            sample_rate_hz = metadata_block.read('uint:20')
            number_of_channels = metadata_block.read('uint:3')
            bits_per_sample = metadata_block.read('uint:5')
            total_samples = metadata_block.read('uint:36')
            audio_data_md5 = metadata_block.read(128)
            if VERBOSE:
                print(' STREAMINFO')
                print('  Bytes: %s' % metadata_block)
                print('  minimum_block_size: %d' % minimum_block_size)
                print('  maximum_block_size: %d' % maximum_block_size)
                print('  minimum_frame_size: %d' % minimum_frame_size)
                print('  maximum_frame_size: %d' % maximum_frame_size)
                print('  sample_rate_hz: %d' % sample_rate_hz)
                print('  number_of_channels: %d' % number_of_channels)
                print('  bits_per_sample: %d' % bits_per_sample)
                print('  total_samples: %d' % total_samples)
                print('  audio_data_md5: %s' % audio_data_md5)

        elif block_type == 1:
            # PADDING
            # No need to actually read it
            metadata_block = read_bitsream(block_length * 8)
            if VERBOSE:
                print(' PADDING')

        elif block_type == 3:
            # SEEKTABLE
            metadata_block = read_bitsream(block_length * 8)
            seektable_count = block_length / 18
            if VERBOSE:
                print(' SEEKTABLE')
                print('  Bytes: %s' % metadata_block)
                print('  Seektable Count: %d' % seektable_count)

            for seektable in range(seektable_count):
                sample_number = metadata_block.read('uint:64')
                offset = metadata_block.read('uint:64')
                number_of_samples = metadata_block.read('uint:16')
                if VERBOSE:
                    print('  SEEKTABLE #%d' % seektable)
                    print('   sample_number: %d' % sample_number)
                    print('   offset: %d' % offset)
                    print('   number_of_samples: %d' % number_of_samples)

        elif block_type == 4:
            # VORBIS_COMMENT
            # http://www.xiph.org/vorbis/doc/v-comment.html
            # 0x200000007265666572656e6365206c696220312e332e3020323031333035323600000000fff8c918
            # 0x200000007265666572656e6365206c6962464c414320312e312e3420323030373032313300000000
            # Note: vendor_length is little endian
            metadata_block = read_bitsream(block_length * 8)
            vendor_length = metadata_block.read('uintle:32')
            vendor_string = metadata_block.read('bytes:32')
            number_of_tags = metadata_block.read('uint:32')
            if VERBOSE:
                print(' VORBIS_COMMENT')
                print('  Bytes: %s' % metadata_block)
                print('  vendor_length: %s' % vendor_length)
                print('  vendor_string: %s' % vendor_string)
                print('  number_of_tags: %s' % number_of_tags)
            # if number_of_tags:
            #    pass
            if number_of_tags == 4294494488:
                print('Fixing known corrupt vendor string')
                vendor_string = 'reference libFLAC 1.3.0 20130526'
                number_of_tags = 0
                POS -= (4 * 8)
                metadata_block = bitstring.pack('uintle:32, bytes:32, uint:32',
                                                vendor_length,
                                                vendor_string,
                                                number_of_tags)

        metadata_blocks += ''.join(metadata_block_header.unpack('bytes'))
        metadata_blocks += ''.join(metadata_block.unpack('bytes'))

        if last_block:
            break

    return metadata_blocks


def read_frames():
    '''Process the FLAC frames in the data in the bitstream'''
    # frames = []

    for fid in xrange(2):
        # <32> frame header
        # <?> variable block size
        frame_header = read_bitsream(40)
        sync_code = frame_header.read('bin:14')
        reserved1 = frame_header.read('bin:1')
        blocking_strategy = frame_header.read('bin:1')
        block_size_in_ic_samples = frame_header.read('bin:4')
        sample_rate = frame_header.read('bin:4')
        channel_assignment = frame_header.read('bin:4')
        sample_size = frame_header.read('bin:3')
        reserved2 = frame_header.read('bin:1')
        crc8 = frame_header.read('bin:8')
        if VERBOSE:
            blocking_strategy_friendly = ' (Fixed)'
            if blocking_strategy == '1':
                blocking_strategy_friendly = ' (Variable)'
            print('Frame Header #%d' % fid)
            print(' Bytes: %s' % frame_header)
            print(' sync_code: %s' % sync_code)
            print(' reserved1: %s' % reserved1)
            print(' blocking_strategy: %s%s' % (blocking_strategy, blocking_strategy_friendly))
            print(' block_size_in_ic_samples: %s' % block_size_in_ic_samples)
            print(' sample_rate: %s' % sample_rate)
            print(' channel_assignment: %s' % channel_assignment)
            print(' sample_size: %s' % sample_size)
            print(' reserved2: %s' % reserved2)
            print(' crc8: %s' % crc8)
        if sync_code != '11111111111110':
            print('ERROR: Bad sync_code')
        if reserved1 != '0':
            print('ERROR: Bad reserved1')
        if block_size_in_ic_samples == '0000':
            print('ERROR: Bad block_size_in_ic_samples')
        if sample_rate == '1111':
            print('ERROR: Bad sample_rate')
        if sample_size == '011':
            print('ERROR: Bad sample_size')
        if sample_size == '111':
            print('ERROR: Bad sample_size')
        if reserved2 != '0':
            print('ERROR: Bad reserved2')

        # frames.append(frame_header)

        # return frames


def main():
    global VERBOSE

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--filename', '-f',
                        default='8cdafe773bf36efe77c88cebceee84f7')
    args = parser.parse_args()

    VERBOSE = args.verbose

    load_data_file(args.filename)

    read_file_magic()

    stream_marker = generate_stream_marker()

    metadata_blocks = read_metadata_blocks()

    read_frames()

    new_bit_stream = bitstring.pack('bytes:4, bytes, bytes',
                                    stream_marker,
                                    metadata_blocks,
                                    DATA[int(POS / 8):])

    f = open('8cdafe773bf36efe77c88cebceee84f7.repaired.flac', 'wb')
    f.write(''.join(new_bit_stream.unpack('bytes')))
    f.close()

main()
