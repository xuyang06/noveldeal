#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/noveldeal/")
os.chdir("/var/www/noveldeal")

from noveldeal import app as application
application.secret_key = 'development key'
