#!/usr/bin/env python

# Example for how to use OptionParser and Logging

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from optparse import OptionParser

parser = OptionParser()
parser.set_defaults(debug=False, logfile='%s.log' % __file__)
parser.add_option('-d', '--debug', dest='debug', action='store_true',
                  help="Turn on debug logging.")
parser.add_option('-l', '--logfile',  dest='logfile',
                  help="Use this file for logging.")
options, args = parser.parse_args()

if options.logfile:
    logging.basicConfig(
        filename=options.logfile,
        format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(
        options.logfile, maxBytes=5e6, backupCount=0)
else:
    handler = StreamHandler()

logger = logging.getLogger(__file__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
if options.debug:
    logger.setLevel(logging.DEBUG)

logger.info("Start logging")
logger.debug("Debug!")
try:
    raise Exception("Exception!")
except:
    logger.exception("Got exception!")
