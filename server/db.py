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
# LICENSE goes here:

# Setup logging
import logging

logging.basicConfig(filename='logs/database.log',level=logging.DEBUG,
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
from config import *
from sqlite3 import dbapi2 as sqlite

########################################################################


# Database Main
class Database():
    
    logging.info('Database Handler: Startup')
        
    @classmethod
    def getAccountData(cls, user, passw):
        
        try:
            # Get connection
            cls.con = sqlite.connect(ACC_DB)
            
            # Setup Cursor
            cls.cur = cls.con.cursor()
            
            # Get the Data from the Table
            cls.cur.execute("""select id, username, password from accounts
                where username=:user and password=:passw""", 
                {"user":user, "passw":passw})
                
            data = cls.cur.fetchone()
            
            logging.info('Connection made to ACCOUNT DB - SUCCESS')
            print "Connection made to ACCOUNT DB - SUCCESS"
            
            return data
                
        except:
            logging.info('Failed to connect to ACCOUNT DB')
            print "Failed to connect to ACCOUNT DB"
            return
        
        
            
            
            
