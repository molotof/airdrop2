#!/usr/bin/python
import sys
import time
import os
import optparse
import json
# update the system path to look for Tool80211 one directory up
import pdb
try:
    import Tool80211
except ImportError:
    # Tool80211 not installed
    # assuming were running out of source directory
    sys.path.append('../')
    try:
        import Tool80211
    except ImportError, e:
        print e
        sys.exit(-1)
    

if __name__ == "__main__":
    print "Airdrop-ng Rule Auto Writer"
    parser = optparse.OptionParser("%prog options [-i]")
    parser.add_option("-i", "--interface", dest="card", nargs=1,
        help="Interface to sniff from")
    parser.add_option("-c", "--channel", dest="channel", nargs=1, default=False,
        help="Interface to sniff from")
    parser.add_option("-e", "--essid", dest="essid", default=None, 
        nargs=1, help="essid to sniff for to find clients")
    parser.add_option("-b", "--bssid", dest="bssid", nargs=1, default=None,
        help="white list a client after it joins this bssid")
    #check for correct number of arguments provided
    if len(sys.argv) < 3:
        parser.print_help()
        print "Calling Example"
        print "python airdropRAW -i wlan0 -e Defcon Secure"
        sys.exit(0)
    else:
        (options, args) = parser.parse_args()
    try:
        """
        create an instance and create vap and monitor
        mode interface
        """
        airmonitor = Tool80211.Airview(options.card)
        airmonitor.start()
        ppmac = airmonitor.pformatMac
        stateTracker = {}
        whitelist = []
        while True:
            """
            run loop every 2 seconds to give us a chance to get new data
            this is a long time but not terrible
            """
            time.sleep(.5)
            # clear the screen on every loop
            os.system("clear")
            """
            grab a local copy from airview thread
            This allows us to work with snapshots and not
            have to deal with thread lock issues
            """
            # empty list for ess tracking
            ess = []
            bss = airmonitor.apObjects 
            # print the current sniffing channel to the screen
            if options.channel is not False:
                airmonitor.hopper.pause()
                print airmonitor.hopper.setchannel(int(options.channel))
            print "Channel %i" %(airmonitor.channel)
            # print out the access points and their essids
            print "Access point"
            for bssid in bss.keys():
                apbssid = ppmac(bssid)
                essid = bss[bssid].essid
                enc = bss[bssid].encryption
                auth = bss[bssid].auth
                channel = bss[bssid].channel
                cipher = bss[bssid].cipher
                oui = bss[bssid].oui
                rssi = bss[bssid].rssi
                print ("%s %s %s %s %s %s %s %s" %(apbssid, essid, enc, cipher, auth, channel, oui, rssi)).encode("utf-8")
                if options.essid is not None:
                    # ess tracking
                    if essid == options.essid:
                        if bssid not in ess:
                            ess.append(bssid)
            """
            Print out the clients and anything they are assoicated to
            as well as probes to the screen
            """
            print "\nClients"
            # get local copies from airview thread
            # local clients
            clients = airmonitor.clientObjects
            # for each client show its data
            for mac in clients.keys():
                # pretty up the mac
                prettymac = ppmac(mac)
                rssi = clients[mac].rssi
                # remove any wired devices we see via wired broadcasts
                if clients[mac].wired is True:
                    continue
                if clients[mac].assoicated is True:
                    assoicatedState = ppmac(clients[mac].bssid)
                else:
                    assoicatedState = clients[mac].bssid
                probes = clients[mac].probes
                oui = clients[mac].oui
                # print out a probe list, otherwise just print the client and its assoication
                if probes != []:
                    print prettymac, assoicatedState, oui, rssi,','.join(probes).encode("utf-8")
                else:
                    print prettymac, assoicatedState, oui, rssi
                # rule logic
                if assoicatedState in ess:
                    #   write kick rule if not in white list
                    #   add to state
                    pass
            # update state counters
            # if counter enough, add to white list
    except KeyboardInterrupt:
        print "\nbye\n"
        airmonitor.kill()
        sys.exit(0)


