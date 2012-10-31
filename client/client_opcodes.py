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

### CLIENT OPCODES ###

# CONNECTION AND LOGIN/CHAT/DISCONNECT
MSG_NONE                        = 0
CMSG_AUTH                       = 1
SMSG_AUTH_RESPONSE              = 2
CMSG_CHAT                       = 3
SMSG_CHAT                       = 4
CMSG_DISCONNECT_REQ             = 5
SMSG_DISCONNECT_ACK             = 6

# GAME STATE STUFF
CMSG_ENTERGAME_REQ              = 7
SMSG_ENTERGAME_ACK              = 8 # Will send some world data aswell
CMSG_EXITTOMENU_REQ             = 9
SMSG_EXITTOMENU_ACK             = 10
CMSG_OLD_POS                    = 11
SMSG_NEW_POS                    = 12

