#!/usr/bin/python

######################################################################## 
# MIT License
#
# Copyright (c) 2012, Martin de Bruyn
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
#----------------------------------------------------------------------#

# Load config
from config import *

# Setup logging
import logging

logging.basicConfig(filename=LOGDIR+'handlers.log',level=logging.DEBUG,
                        format='%(asctime)s: %(message)s')
## LOGGING Guide:
#
#  logging.debug('This message should go to the log file')
#  logging.info('So should this')
#  logging.warning('And this, too')
#
#################################

## IMPORTS ##
import os
import sys

### PANDA Imports ###
from pandac.PandaModules import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task.Task import Task


## Client Imports ##
from client_opcodes import *


########################################################################
########################################################################


### MAIN HANDLER CLASS ###
#----------------------------------------------------------------------#
# HANDLER (TCP focused)
#----------------------------------------------------------------------#

class Handler():
    """
    This class will keep all the handler methods, for each type opcode
    regarding simple tasks and mainly tcp based
    """
    
    def __init__(self, _base):
        
        logging.info('Handler Loaded')
        print "Handler Loaded"
        self.network = _base
        self.tcpConn = self.network.tcpConnection
    
    
    
    def auth_REQ(self, user, passw):
        """
        Handle the login packet to server.
        """
        # Create the buffer
        pkg = PyDatagram()
        
        # Add the opcode
        pkg.addUint16(CMSG_AUTH)
        
        # Add the user and pass Details
        # This is kept really simple
        pkg.addString(user)
        pkg.addString(passw)
        
        # Send the packet
        self.network.tcpWriter.send(pkg, self.tcpConn)
        
        
    
    def handleAuth_Response(self, opcode, data):
        """
        Handle the smsg regarding Auth between client and server
        Note: This is really simple.
        """
        # Get the flag the server sends
        flag = data.getUint16()
        
        # Do a check
        if flag == 0:
            print "Username doesn't exist!"
            self.network.game.gui.login_gui.popError4()
            
        if flag == 2:
            print "Login incorrect..."
            # Update the login screen with a msg.
            self.network.game.gui.login_gui.popError1()
        
        if flag == 1:
            print "Login successful"
            # Move to the main menu
        


#----------------------------------------------------------------------#
# HANDLER END
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
# GAME HANDLER (UDP focused)
#----------------------------------------------------------------------#

class GameHandler():
    """
    This class will keep all the handler methods for each type opcode,
    regarding the in game/gameplay stuff, udp based.
    """
    
    def __init__(self, _base):
        
        logging.info('GameHandler Loaded')
        print "GameHandler Loaded"
        self.network = _base











