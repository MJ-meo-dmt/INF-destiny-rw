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
#----------------------------------------------------------------------#

# Setup logging
import logging

logging.basicConfig(filename='logs/network.log',level=logging.DEBUG,
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
from panda3d.core import Vec3
from direct.showbase.DirectObject import DirectObject


# Client Imports
from config import *
from handlers import Handler
from handlers import GameHandler
from client_opcodes import *


########################################################################
########################################################################

# Client Network

class Network():
    
    def __init__(self, _base):
        
        # Game base
        self.game = _base
        
        # Login state
        self.LOGGED = False
        
        ### SETUP NETWORKING ###
        
        ## TCP Connection ##
        self.tcpConnection = None
        
        ## TCP NETWORKING ##
        
        # TCP Manager
        self.tcpManager = QueuedConnectionManager()
        
        # TCP Listener
        self.tcpListener = QueuedConnectionListener(self.tcpManager, 0)
        
        # TCP Reader
        self.tcpReader = QueuedConnectionReader(self.tcpManager, 0)
        
        # TCP Writer
        self.tcpWriter = ConnectionWriter(self.tcpManager, 0)
        
        
        ## UDP NETWORKING ##
        
        # UDP Manager
        self.udpManager = QueuedConnectionManager()
        
        # UDP Reader
        self.udpReader = QueuedConnectionReader(self.udpManager, 0)
        
        # UDP Writer
        self.udpWriter = ConnectionWriter(self.udpManager, 0)
        
        
        ### SETUP HANDLER INSTANCE ###
        self.handler = Handler(self)
        self.gameHandler = GameHandler(self)
        
        
        ### SETUP HANDLERS DICT ###
        self.HandlerDict = {}
        
        
        ### SETUP NETWORKING TASKS ###
        
        # TCP ReaderTask
        taskMgr.add(self.tcpReaderTask, "ClientTCPReaderTask", -40)
        # UDP ReaderTask
        taskMgr.add(self.udpReaderTask, "ClientUDPReaderTask", -39)
        
        
        
#----------------------------------------------------------------------#
# NETWORK TASKS TCP MAIN
#----------------------------------------------------------------------#
    def tcpReaderTask(self, task):
        """
        Handle data from server.
        """
        while 1:
            (datagram, data, opcode) = self.tcpNonBlockingRead(self.tcpReader)
            if opcode is MSG_NONE:
                # Do nothing
                break
            else:
                self.tcpHandleDatagram(data, opcode)
        
        return Task.cont
        
    
    def tcpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on 
        the queued tcp connection reader.
        
        @param qcr: self.tcpReader
        """
        if self.tcpReader.dataAvailable():
            datagram = NetDatagram()
            if self.tcpReader.getData(datagram):
                data = PyDatagramIterator(datagram)
                opcode = data.getUint16()
            else:
                data = None
                opcode = MSG_NONE
        else:
            datagram = None
            data = None
            opcode = MSG_NONE
            
        return (datagram, data, opcode)
        
    
    def tcpHandleDatagram(self, data, opcode):
        """
        Check for the handle assigned to the opcode.
        """
        if opcode in self.HandlerDict.keys():
            self.HandlerDict[opcode](opcode, data)
        else:
            logging.info("Unknown opcode received: %d", opcode)
            print "Unknown opcode: %d" % opcode
            print data
        return

#----------------------------------------------------------------------#
# NETWORK TASKS TCP END
#----------------------------------------------------------------------#
        
        
#----------------------------------------------------------------------#
# NETWORK TASKS UDP MAIN
#----------------------------------------------------------------------#
    def udpReaderTask(self, task):
        """
        Handle any data from server on udp port.
        """
        while 1:
            (datagram, data, opcode) = self.udpNonBlockingRead(self.udpReader)
            if opcode is MSG_NONE:
                # Do nothing
                break
            else:
                # Got some data handle it
                self.udpHandleDatagram(data, opcode)
        
        return Task.cont
    
    
    def udpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on
        the queued connection udpReader
        """
        if self.udpReader.dataAvailable():
            datagram = NetDatagram()
            if self.udpReader.getData(datagram):
                data = PyDatagramIterator(datagram)
                opcode = data.getUint16()
            else:
                data = None
                opcode = MSG_NONE
        else:
            datagram = None
            data = None
            opcode = MSG_NONE
            
        # Return the datagram to keep a handle on the data
        return (datagram, data, opcode)
        
    
    def udpHandleDatagram(self, data, opcode):
        """
        Check for the handler assigned to the opcode.
        """
        if opcode in self.HandlerDict.keys():
            self.HandlerDict[opcode](opcode, data)
        else:
            logging.info("Unknown opcode received: %d", opcode)
            print "Unknown opcode received: %d" % opcode
            print data 
        return

#----------------------------------------------------------------------#
# NETWORK TASKS UDP END
#----------------------------------------------------------------------#
 
 
    def doLogin(self):
        """
        Handle the login state for the client when the player enters
        the user/pass info
        """
        try:
            self.LOGGED = True
            self.tcpConnection = self.tcpManager.openTCPClientConnection(IP, tcpPORT, TIMEOUT)
            self.tcpReader.addConnection(self.tcpConnection)
            print "Connected"
            # Add something here to change the status text in the login screen
            
        except:
            self.LOGGED = False
            print "Connection to server failed, Server offline..."

















