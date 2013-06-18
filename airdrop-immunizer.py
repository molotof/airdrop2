#!/usr/bin/python
#################################################
#						#
# Creates a new allow rule for the incoming mac #
#						#
#################################################
#immunizer [lan or mac]
import json
import sys
import os
import re
from get_mac import *
import pdb

# Ripped this out of the wifiobjects from py, because it was simpler...bad crypt0s.
class accessPoint:
    """
    Access point object
    """
    def __init__(self, bssid):
        self.ruletype = "allow"
        self.attack = "0"
        self.type = "access_point"
        # set first time seen
        self.bssid = bssid          # bssid of ap

class client:
    """
    Client object
    """
    def __init__(self, mac):
        """
        mac = client mac address in hex   
        """
        self.ruletype = "allow"
        self.attack = "0"
        self.type = "client"
        self.mac = mac                # client mac address
        self.bssid = None             # Bssid of assoicated ap


if len(sys.argv) == 1:
    print "Usage:"
    print "airdrop-immunizer.py [mac/interface] [filename]"
    print ""
    print "Adds onto an existing airdrop configuration file with an allow rule for whatever mac/interface you specified, immunizing it from targeting."
    print ""
    exit()
# if we see ':' then we assume it's a mac address
if ':' in sys.argv[1]:
    pass
    #mac = sys.argv[1].replace(':','').decode('hex')
# If we don't, then it must have been the name of an interface - get it's mac address.
else:
    mac = get_mac(sys.argv[1])#.replace(':','').decode('hex')
data = {}

# Create objects out of wifiobjects -- they have all the things we track already, not that we need them (yet, this code will be extended to the rulebuilder)
immuneap = accessPoint(mac)
# Add the aspects of the object that are ONLY found in the RULE class
immuneap.ruletype = "allow"
immuneap.attack = "0"
immuneap.type = "ap"

# The same as above, but for a client. We create both just because it's easy.
immuneclient = client(mac)
immuneclient.ruletype = "allow"
immuneclient.attack = "0"
immuneclient.type = "client"
immuneclient.bssid = mac

filename = sys.argv[2]
file_exists = os.path.exists(filename)
# Open the filename and write changes
if file_exists:
    with open(filename,'r') as conffile:
        pdb.set_trace()
        # Determine if the file exists and if it does, open it as a json object.
        try:
            data = json.load(conffile)
        except:
            print "File did not contain rules already or did not exist, writing new rules file to " + filename

data['ap'+mac] = immuneap.__dict__
data['client'+mac] = immuneclient.__dict__
del data['client'+mac]['apObject']

# Remove the Nones and replace with ""
# Note: does it matter if it's "" vs null when parsed by the rule parser and compared on the match?!
for rule in data.keys():
    for key in data[rule]:
        if data[rule][key] == None or key == 'fts': #must also remove the fts value that is generated.
            data[rule][key] = ""

with open(filename,'w') as conffile:
    conffile.write(json.dumps(data))
    print str(sys.argv[1]) + " immunization written to config file at " + filename

# I may have to make my own ap and client wifiobject stubs here in order to keep the peace.    
