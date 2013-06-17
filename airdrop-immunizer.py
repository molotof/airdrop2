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
from wifiobjects import *
import pdb

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

# Create objects out of wifiobjects -- they have all the things we track already, not that we need them (yet, this code will be extended to the rulebuilder)
immuneap = accessPoint(mac)
# Add the aspects of the object that are ONLY found in the RULE class
immuneap.ruletype = "allow"
immuneap.attack = "0"
immuneap.type = "access_point"

# The same as above, but for a client. We create both just because it's easy.
immuneclient = client(mac)
immuneclient.ruletype = "allow"
immuneclient.attack = "0"
immuneclient.type = "client"

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
#class accessPoint:
#    """
#    Access point object
#    """
#    def __init__(self, bssid):
#        self.ruletype = "allow"
#        self.attack = "0"
#        self.type = "access_point"
#        # set first time seen
#        self.fts = time.time()      # first time object is seen
#        self.lts = None             # last time object is seen, update on every acccess
#        self.connectedClients = []  # list of connected clients
#        self.essid = None           # broadcasted essid
#        self.bssid = bssid          # bssid of ap
#        self.hidden = False         # denote if essid is hidden
#        self.encryption = None      # show encryption level
#        self.auth = None            # show authentication settings
#        self.cipher = None          # cipher, either CCMP, TKIP, wep 64/128
#        self.channel = None         # ap's channel
#        self.ssidList = []          # rolling list of seen ssid's for this ap
#        self.oui = self.populateOUI() # lookup the object oui
#
#class client:
#    """
#    Client object
#    """
#    def __init__(self, mac):
#        """
#        mac = client mac address in hex   
#        """
#        self.ruletype = "allow"
#        self.attack = "0"
#        self.type = "client"
#        self.fts = time.time()        # first time object is seen
#        self.lts = None               # last time object is seen, update on every access 
#        self.mac = mac                # client mac address
#        self.probes = []              # list of probe requests client broadcast
#        self.assoicated = False       # list if client is associated to an ap
#        self.bssid = None             # Bssid of assoicated ap
#        self.wired = False            # not a wired client by default
#        self.lastBssid = None         # last connected bssid
#        self.managedFrame = False     # have we seen a managment frame from this client?
#        self.oui = self.populateOUI() # populate clients oui lookup#
#        self.apObject = None          # stores reference link to ap# object when connected to bssid

