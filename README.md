magstripe
=========

A small utility to handle reading and writing magnetic stripe cards over serial.
Tested with the SparkFun SEN-08634, but may work for other writers as well.

Prerequisites
-------------
* Python 3.x
* [pyserial](http://pyserial.sourceforge.net/)

Usage
-----

### Reading a card
1. `chmod 0666 /dev/ttyUSB0`
2. `./magstripe.py /dev/ttyUSB0`

### Writing to a card
1. `chmod 0666 /dev/ttyUSB0`
2. `echo ";1234567890?" | ./magstripe.py -w /dev/ttyUSB0`
