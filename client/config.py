#!/usr/bin/python

######################################################################## 
# MIT License
#
# Copyright (c) <2012>, <Martin de Bruyn>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
########################################################################

## SYSTEM IMPORTS ##
import sys
import os
import ConfigParser

### CONFIG LOADER ###

config = ConfigParser.RawConfigParser()
config.read('client.cfg')

# CLIENT NETWORKING #
tcpPORT = config.getint('CLIENT', 'tcpport')
TIMEOUT = config.getint('CLIENT', 'timeout')
IP = config.get('CLIENT', 'ip')
udpPORT = config.getint('CLIENT', 'udpport')


# CLIENT PLAYER SETTINGS #
FORWARD = config.get('CONTROLS', 'forward')
BACKWARD = config.get('CONTROLS', 'backward')
SIDE_L = config.get('CONTROLS', 'side_l')
SIDE_R = config.get('CONTROLS', 'side_r')

# LOG DIR #
LOGDIR = "logs/"












