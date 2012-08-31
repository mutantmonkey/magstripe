#!/usr/bin/python3
################################################################################
# magstripe.py - serial magstripe card reader/writer utility
# A small utility to handle reading and writing magnetic stripe cards over
# serial. Available under the ISC license.
#
# https://github.com/mutantmonkey/magstripe
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import argparse
import serial
import struct
import sys

__author__ = "mutantmonkey <mutantmonkey@mutantmonkey.in>"
__license__ = "ISC"


class Constants(object):
    def __init__(self, values):
        self.values = dict(values)

    def __getattr__(self, name):
        if name.endswith('_BYTE'):
            return self.values[name[:-5]]
        else:
            return struct.pack('B', self.values[name])


constants = Constants([
    ('STX', 2),
    ('ETX', 3),
    ('CR',  21),

    ('ARM_RAW_WRITE',   96),

    ('TRACK1_START',    37),    # %
    ('TRACK1_SEP',      94),    # ^
    ('TRACK1_END',      63),    # ?
    ('TRACK2_START',    59),    # ;
    ('TRACK2_SEP',      61),    # =
    ('TRACK2_END',      63),    # ?
    ('TRACK3_START',    43),    # +
    ('TRACK3_SEP',      36),    # $
    ('TRACK3_END',      63),    # ?
])


def read_track(buf, start_byte, sep_char, end_char, skip=0):
    track = buf[1:-1]
    output = None
    if len(track) > 0 and track[0] == start_byte:
        end = track.find(end_char)
        fields = track[1 + skip:end]
        fields = fields.split(sep_char)
        output = [field.decode('ascii') for field in fields]
        buf = buf[end + 1:]
        track = buf[1:-1]
    return output, buf

parser = argparse.ArgumentParser(description="A small utility to handle "\
        "reading and writing magnetic stripe cards over serial.")
parser.add_argument('device', help="Serial device to use.")
parser.add_argument('-b', '--baud', dest='baud', default=9600, type=int,
        help="Baud rate for the serial device.")
parser.add_argument('-l', '--log', dest='log', default=None,
        help="Log file to dump raw magstripe output to.")
parser.add_argument('-w', '--write', dest='write', default=False,
        action="store_true", help="Write input from stdin to magstripe card.")

args = parser.parse_args()

with serial.Serial(args.device, args.baud) as ser:
    if args.write:
        data = sys.stdin.read()
        data = data.strip()

        if data:
            ser.write(constants.STX)
            ser.write(constants.ARM_RAW_WRITE)
            ser.write(constants.ETX)

            ser.write(constants.STX)
            ser.write(data.encode('ascii'))
            ser.write(constants.ETX)
        else:
            raise Exception("No data specified on stdin to write.")

        buf = b""
        c = b""
        while c != constants.ETX:
            c = ser.read()
            buf += c
        if c == constants.ETX and buf[1:-1] == data.encode('ascii'):
            print("Card written.")
        else:
            raise Exception("Failed to write to card.")
    else:
        buf = b""
        try:
            while True:
                c = ser.read()
                buf += c

                if c == constants.ETX:
                    buf = buf.strip(constants.CR)
                    track = buf[1:-1]

                    if args.log:
                        with open(args.log, 'a') as f:
                            f.write(track.decode('ascii') + "\n")

                    # Track 1
                    output, buf = read_track(buf, constants.TRACK1_START_BYTE,
                            constants.TRACK1_SEP, constants.TRACK1_END)
                    if output:
                        print("Track 1: " + str(output))

                    # Track 2
                    output, buf = read_track(buf, constants.TRACK2_START_BYTE,
                            constants.TRACK2_SEP, constants.TRACK2_END)
                    if output:
                        print("Track 2: " + str(output))

                    # Track 3
                    output, buf = read_track(buf, constants.TRACK3_START_BYTE,
                            constants.TRACK3_SEP, constants.TRACK3_END)
                    if output:
                        print("Track 3: " + str(output))

                    buf = b""
                    print()
        except KeyboardInterrupt:
            pass
