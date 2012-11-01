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


## IMPORTS ##
import os
import sys

### PANDA Imports ###
from pandac.PandaModules import *
from panda3d.rocket import *
from direct.showbase.DirectObject import DirectObject

# Client Imports
from handlers import Handler


########################################################################
########################################################################


### MAIN GUI CLASS ###

class Gui():
	
	def __init__(self, _base):
		
		self.game = _base
				
		## Load a font type ##
		LoadFontFace("gui_data/Delicious-Roman.otf")
		
		## Setup a librocket and the input handler ##
		rw = RocketRegion.make('pandaRocket', base.win)
		rw.setActive(1)
		
		# Handler
		ih = RocketInputHandler()
		base.mouseWatcher.attachNewNode(ih)
		rw.setInputHandler(ih)
		
		# Setup context
		self.context = rw.getContext()
		
		## LOAD THE LOGIN SCREEN ##
		self.load_login()
	
		
	def load_Main_menu(self):
		
		self.main_menu = Main_menu(self)
		
	
	def load_login(self):
		
		self.login_gui = Login(self)
	
	
	def removeMain_menu(self):
		"""
		Handle the removal of the main_menu_gui.
		"""
		self.main_menu_gui.remove()
	
	
	def removeLogin(self):
		"""
		Handle the removal of the LoginScreen_gui.
		"""
		self.login_gui.remove()
		

class Login(DirectObject):
	
	def __init__(self, _Gui):
		
		self.gui = _Gui
		
		# Setup Login Screen gui
		self.login_gui = self.gui.context.LoadDocument('gui_data/login.rml')
		self.login_gui.Show()
		
		## LISTEN FOR EVENTS ##
		# From the login.rml file, the user/pass gets send here.
		self.accept('Login_attempt', self.loginAttempt)
	
	
	### THE ERRORS COULD BE DONE BETTER :P
	# User/passw incorrect
	def popError1(self):
		status = self.login_gui.GetElementById('error2')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error3')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error4')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error1')
		status.style.display = "block"
	
	# Fill in all fields
	def popError2(self):
		status = self.login_gui.GetElementById('error1')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error3')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error4')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error2')
		status.style.display = "block"
	
	# Can't connect to server
	def popError3(self):
		status = self.login_gui.GetElementById('error1')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error2')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error4')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error3')
		status.style.display = "block"
		
	# Username Doesn't exist
	def popError4(self):
		status = self.login_gui.GetElementById('error1')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error2')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error3')
		status.style.display = "none"
		
		status = self.login_gui.GetElementById('error4')
		status.style.display = "block"

	def loginAttempt(self, user, passw):
		
		# Try login
		if user == "":
			self.popError2()
		elif passw == "":
			self.popError2()
		
		elif user and passw != "":
			
			print "Attemting Login..."
			self.gui.game.NetworkBase.makeConnection()
			self.gui.game.NetworkBase.handler.auth_REQ(user, passw)
				

	def remove(self):
		
		self.login_gui.Close()



	
		
#----------------------------------------------------------------------#
# GUI - MAIN MENU
#----------------------------------------------------------------------#

class Main_menu():
	
	def __init__(self, _Gui):
		
		self.gui = _Gui
		
		self.menu_gui = self.gui.context.LoadDocument('gui_data/main_menu.rml')
		self.menu_gui.Show()
		
		
























