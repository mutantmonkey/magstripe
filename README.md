magstripe
=========

A small utility to handle reading and writing magnetic stripe cards over serial.

Prerequisites
-------------
* Python 3.x
* [pyserial](http://pyserial.sourceforge.net/)

Usage
-----

### Reading a card
1. `chmod 0666 /dev/ttyUSB0`
2. `magstripe/magstripe.py /dev/ttyUSB0`

### Writing to a card
1. `chmod 0666 /dev/ttyUSB0`
2. `echo ";1234567890?" | magstripe/magstripe.py -w /dev/ttyUSB0`
