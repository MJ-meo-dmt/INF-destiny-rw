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

# Server Network config file load.
logging.info('Loading Server cfg')
try:
    from config import *
    logging.info('Server cfg: Loaded')
except:
    print "Error while trying to load Server cfg-file!"
    logging.warning('Server cfg load error, check config file!')


### PANDA Imports ###
from pandac.PandaModules import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task.Task import Task


## Server Imports ##
from handlers import Handler
from handlers import GameHandler
from server_opcodes import *

########################################################################
########################################################################


### MAIN SERVER NETWORK CLASS ###

class Network():
    
    def __init__(self, _base):
        
        # Add Base (GameServer)
        self.base = _base
        
        ## SETUP TCP Networking ##
        
        # Connection Manager for Tcp
        self.tcpManager = QueuedConnectionManager()
        
        # Tcp listener
        self.tcpListener = QueuedConnectionListener(self.tcpManager, 0)
        
        # Tcp Reader
        self.tcpReader = QueuedConnectionReader(self.tcpManager, 0)
        
        # Tcp Writer
        self.tcpWriter = ConnectionWriter(self.tcpManager, 0)
        
        
        ## SETUP UDP Networking ##
        
        # Connection Manager for Udp
        self.udpManager = QueuedConnectionManager()
        
        # Udp Reader
        self.udpReader = QueuedConnectionReader(self.udpManager, 0)
        
        # Udp Writer
        self.udpWriter = ConnectionWriter(self.udpManager, 0)
        
        
        ## SETUP Sockets ##
        
        # TCP Socket
        self.tcpSocket = self.tcpManager.openTCPServerRendezvous(tcpPORT, BACKLOG)
        
        # Add the TCP socket to the listener to listen for new connections
        self.tcpListener.addConnection(self.tcpSocket)
        
        # UDP Socket
        self.udpSocket = self.udpManager.openUDPConnection(udpPORT)
        
        ## INSTANCE HANDLER CLASS ##
        # Basic handler
        self.handler = Handler(self)
        # Gameplay handler
        self.gameHandler = GameHandler(self)
#----------------------------------------------------------------------#
# NETWORK HANDLERS
#----------------------------------------------------------------------#
        ### SETUP HANDLERS FOR OPCODES ###
        self.HandlerDict = {
            CMSG_AUTH            : self.handler.handleAuth,
            CMSG_DISCONNECT_REQ  : self.handler.handleDisconnect
            }
#----------------------------------------------------------------------#
# NETWORK HANDLERS END
#----------------------------------------------------------------------#
 
 
#----------------------------------------------------------------------#
# NETWORK TASK MANAGER STARTUP
#----------------------------------------------------------------------#
        ### ADD NETWORK TASKS TO MANAGER ###
        # TCP
        taskMgr.add(self.tcpListenerTask, "Server_tcpListenerTask", -40)
        logging.info('TCP Listener Started')
        taskMgr.add(self.tcpReaderTask, "Server_tcpReaderTask", -39)
        logging.info('TCP Reader Started')
        
        # UDP
        taskMgr.add(self.udpReaderTask, "Server_udpReaderTask", -39)
        logging.info('UDP Reader Started')
#----------------------------------------------------------------------#
# NETWORK TASK MANAGER STARTUP END
#----------------------------------------------------------------------#
        
        
#----------------------------------------------------------------------#
# NETWORK TASKS TCP MAIN
#----------------------------------------------------------------------#
    ## TCP Listener Task ##
        
    def tcpListenerTask(self, task):
        """
        Accept new incoming connection from clients, related to TCP
        """
            
        # Handle new connection
        if self.tcpListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
                
            if self.tcpListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                
                # Tell the reader about the new TCP connection
                self.tcpReader.addConnection(newConnection)
                self.base.ACTIVECON.append(newConnection)
                    
                logging.info('New Connection: %s + %s', newConnection, netAddress.getIpString())
                print "New Connection: ", str(netAddress.getIpString())
            else:
                print "Connection Failed from: ", str(netAddress.getIpString())    
                    
            
        return Task.cont
        
        
    ## TCP READ TASK ##
    def tcpReaderTask(self, task):
        """
        Handle any data from clients by sending it to the Handlers.
        """
            
        while 1:
            (datagram, data, opcode) = self.tcpNonBlockingRead(self.tcpReader)
            if opcode is MSG_NONE:
                # Do nothing or use it as some 'keep_alive' thing.
                break 
            else:
                # Handle it
                self.tcpHandleDatagram(data, opcode, datagram.getConnection())
                
        return Task.cont
            
            
    ## TCP nonBlockingRead ##
    def tcpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on
        the queued connection tcpReader
        
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
            
        # Return the datagram to keep a handle on the data
        return (datagram, data, opcode)
            
        
    ## TCP handleDatagram ##
    def tcpHandleDatagram(self, data, opcode, client):
        """
        Check for the handle assigned to the opcode.
        """
        if opcode in self.HandlerDict.keys():
            self.HandlerDict[opcode](opcode, data, client)
        else:
            logging.info("WRONG opcode received: %d, from %s", opcode, client)
            print "WRONG opcode: %d" % opcode
            print data
            
        return
        
#----------------------------------------------------------------------#
# NETWORK TASKS TCP MAIN END
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
# NETWORK TASKS UDP MAIN
#----------------------------------------------------------------------#
        
    # UDP Reader 
    def udpReaderTask(self, task):
        """
        Handle any data from udp clients.
        On port <port conf>
        """
        while 1:
            (datagram, data, opcode) = self.udpNonBlockingRead(self.udpReader)
            if opcode is MSG_NONE:
                # Nothing todo
                break 
            else:
                # Got data and handle it.
                self.udpHandleDatagram(data, opcode, datagram.getConnection())
            
        return Task.cont 
        
        
    # UDP nonBlockingRead
    def udpNonBlockingRead(self, qcr):
        """
        Return a datagram collection and type if data is available on
        the queued connection udpReader.
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
            
        
    # UDP handledatagram
    def udpHandleDatagram(self, data, opcode, client):
        """
        Check for the handler assigned to the opcode.
        """
        if opcode in self.HandlerDict.keys():
            self.HandlerDict[opcode](opcode, data, client)
        else:
            logging.info("Unknown opcode received: %d, from: %s", opcode, CLIENTS[client])
            print "Unknown opcode: %d" % opcode
            print data 
        return
            
#----------------------------------------------------------------------#
# NETWORK TASKS UDP MAIN END
#----------------------------------------------------------------------#








