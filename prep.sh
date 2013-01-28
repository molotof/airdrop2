#!/bin/bash

killall wicd
killall dhclient
killall wpa_supplicant
killall wpa_cli
killall ifplugd

echo "Interface: "

read iface

ifconfig $iface down

echo "The interface should be down.  Check it then press enter. If it's still up, you have other programs running the wifi"
read pause

ifconfig $iface up

echo "You're good to go."
