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

logging.basicConfig(filename=LOGDIR+'server.log',level=logging.DEBUG,
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
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject

## Server Imports ##
from servernetwork import Network

########################################################################
########################################################################


### MAIN GAMESERVER CLASS ###

class GameServer(ShowBase):
    
    def __init__(self):
        
        # Set console only mode
        ShowBase(windowType = 'none')
        
        logging.info('Game Server Startup...')
        self.accept('escape', self.serverShutdown)
        
        print """
        ################################################################
        ##                                                            ##
        ##  DESTINY SERVER                                            ##
        ##                                                            ##
        ##  ver. 01                                                   ##
        ################################################################
        """
#----------------------------------------------------------------------#
# SERVER GLOBALS
#----------------------------------------------------------------------#

        # List Active Socket connections
        self.ACTIVECON = []

        # Store Active Players
        # This stores the Player class instance for each player in the world.
        self.PLAYERS = {}

#----------------------------------------------------------------------#
# SERVER GLOBALS END
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
# SERVER GAME WORLD
#----------------------------------------------------------------------#
        ###  INSTANCE GAME WORLD HERE  ###
        print "Starting up without World..."
        
        
#----------------------------------------------------------------------#
# SERVER GAME WORLD END
#----------------------------------------------------------------------#



#----------------------------------------------------------------------#
# SERVER NETWORKING
#----------------------------------------------------------------------#
        ### SETUP NETWORKING ###
        self.network = Network(self)
        print "Network Loaded..."
        
#----------------------------------------------------------------------#
# SERVER NETWORKING END
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
# SERVER SHUTDOWN
#----------------------------------------------------------------------#
    def serverShutdown(self):
        
        # Send a msg to all the clients regarding the server being
        # shutdown, maybe add some timer on it?
        
        # Get the clients connected
        for client in self.ACTIVECON:
            
            self.ACTIVECON.remove(client)
            self.network.tcpReader.removeConnection(client)
            
        sys.exit()

GS = GameServer()
run()
        
       
        
        
        
        



















