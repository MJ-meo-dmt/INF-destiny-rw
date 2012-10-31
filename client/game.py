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

logging.basicConfig(filename='logs/client.log',level=logging.DEBUG,
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

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""    
	window-title Destiny - Client  v.01
	fullscreen 0
	win-size 1024 768
	cursor-hidden 0
	show-frame-rate-meter 1
"""
)

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject


# Client Imports
from network import Network




########################################################################
########################################################################


# Game Client Main class

class Game(ShowBase):
	
	def __init__(self):
		
		self.name = "Game"
		
		logging.info("Client Started")
		print "Client Started"
		
		# Start showbase(panda)
		ShowBase.__init__(self)
		
		# Exit on esc
		self.accept('escape', self.quit)
		
		# Start login screen
		
		# Start Network
		self.NetworkBase = Network(self)
		
	
	def quit(self):
		
		try:
			print "Disconnect from server"
			return False
			# Do handler send to server req dc
			
		except:
			sys.exit()
			


game = Game()

run()








	

