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


## Server Imports ##
from db import Database
from player import Player
from server_opcodes import *

########################################################################
########################################################################


### MAIN HANDLER CLASS ###
#----------------------------------------------------------------------#
# HANDLER (TCP focused)
#----------------------------------------------------------------------#

class Handler():
    """
    This class will keep all the handler methods, for each type opcode.
    Regarding the login and other simple tasks.
    """
    
    def __init__(self, _baseNet):
        
        logging.info('Handler Loaded')
        self.baseNet = _baseNet
        
#----------------------------------------------------------------------#
# HANDLE AUTH
#----------------------------------------------------------------------#
    def handleAuth(self, opcode, data, client):
        """
        Handle auth and player login.
        NOTE: THIS IS REALLY SIMPLE FOR NOW
        Add something to check if the user is already logged in
        """
        
        # Get the data the client sent.
        clientUser = data.getString()
        clientPass = data.getString()
        
        # Flag to be send back after serverside auth
        flag = None
        userpass = False
        loginTries = 0 # Not thought out now, will return to it later...
        
        # Get the data from DB
        try:
            # Here we can add the player to the PLAYERS{} by using a player
            # ID or something
            details = []
            details = Database.getAccountData(clientUser, clientPass)
        
        except:
            print "Can't connected to ACCOUNT DATABASE"
        
        # Will make some other checks later... this is just good for now..
        if details == None:
            flag = 2
            print "Player: ", clientUser, " Doesn't exist! or Incorrect!"
            loginTries += 1
            
        # Check if the password/username match
        elif clientPass == details[2] and clientUser == details[1]:
            print details
            userpass = True
            self.baseNet.base.PLAYERS[details[0]] = Player(self, details[0], details[1])
            print "Player: ", details[1], " Logged in, ID: ", details[0]
            flag = 1
                
        else:
            userpass = False
            print "Player: ", clientUser, " login incorrect"
            loginTries += 1
            flag = 2
            
        # Create buffer
        pkg = PyDatagram()
        
        # Add response
        pkg.addUint16(SMSG_AUTH_RESPONSE)
        
        # Add the flag
        pkg.addUint16(flag)
        
        # Send the packet
        self.baseNet.tcpWriter.send(pkg, client)
            
            
#----------------------------------------------------------------------#
# HANDLE DISCONNECT
#----------------------------------------------------------------------#
    def handleDisconnect(self, opcode, data, client):
        """
        Handle disconnection for clients.
        """
        # create buffer
        pkg = PyDatagram()
        
        # Add opcode
        pkg.addUint16(SMSG_DISCONNECT_ACK)
        
        # Send the packet
        self.baseNet.tcpWriter.send(pkg, client)
        self.baseNet.base.ACTIVECON.remove(client)
        logging.info("Client: %s, Disconnected", client)
        print "Client: %s, Disconnected" % client
        
        # Remove the connection from the tcpReader
        self.baseNet.tcpReader.removeConnection(client)
        

#----------------------------------------------------------------------#
# HANDLER END
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
# GAME HANDLER (UDP focused)
#----------------------------------------------------------------------#

class GameHandler():
    """
    This class will keep all the handler methods for each type opcode,
    regarding the in game/gameplay.
    """
    
    def __init__(self, _base):
        
        logging.info('GameHandler Loaded')
        self.base = _base










