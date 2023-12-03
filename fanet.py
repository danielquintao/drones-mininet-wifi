import os
import sys
import time
import threading
import logging


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.replaying import ReplayingMobility
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference

from server import create_app


def topology():
    "Create a network."
    global net
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02',
                          ip='10.0.0.1/8', speed=1, inNamespace=False) #! inNamespace=False is necessary for drone to access Flask HTTP server that we'll
                                                                       #! create in the root namespace
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03',
                          ip='10.0.0.2/8', speed=1, inNamespace=False)
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04',
                          ip='10.0.0.3/8', speed=1, inNamespace=False)
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05',
                          ip='10.0.0.4/8', speed=1, inNamespace=False)
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:06',
                          ip='10.0.0.5/8', speed=1, inNamespace=False)
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:07',
                          ip='10.0.0.6/8', speed=1, inNamespace=False)
    sta7 = net.addStation('sta7', mac='00:00:00:00:00:08',
                          ip='10.0.0.7/8', speed=1, inNamespace=False)
    sta8 = net.addStation('sta8', mac='00:00:00:00:00:09',
                          ip='10.0.0.8/8', speed=1, inNamespace=False)
    sta9 = net.addStation('sta9', mac='00:00:00:00:00:10',
                          ip='10.0.0.9/8', speed=1, inNamespace=False)
    
    p2 = net.addAccessPoint("p2", mac='00:00:00:00:00:20')
    p3 = net.addAccessPoint("p3",  mac='00:00:00:00:00:30')
    p2.lastpos = (50,50,0)
    p2.position = (50,50,0)
    p3.position = (70,70,0)
    p3.lastpos = (70,70,0)

    sz1 = net.addAccessPoint("sz1", mac='00:00:00:00:00:40')
    sz2 = net.addAccessPoint("sz2", mac='00:00:00:00:00:50')
    sz3 = net.addAccessPoint("sz3", mac='00:00:00:00:00:60')
    
    sz1.lastpos = (35.0, 27.0, 0)
    sz1.position = (35.0, 27.0,0)
    sz2.position = (85.0, 55.0,0)
    sz2.lastpos = (85.0, 55.0,0)
    sz3.position = (15.0, 65.0,0)
    sz3.lastpos = (15.0, 65.0,0)


    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring nodes\n")
    net.configureNodes()


    info("*** Creating links\n")
    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0', ssid='adhocNet')
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0', ssid='adhocNet')
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0', ssid='adhocNet')
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0', ssid='adhocNet')
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0', ssid='adhocNet')
    net.addLink(sta6, cls=adhoc, intf='sta6-wlan0', ssid='adhocNet')
    net.addLink(sta7, cls=adhoc, intf='sta7-wlan0', ssid='adhocNet')
    net.addLink(sta8, cls=adhoc, intf='sta8-wlan0', ssid='adhocNet')
    net.addLink(sta9, cls=adhoc, intf='sta9-wlan0', ssid='adhocNet')

    net.isReplaying = True
    set_pos(sta1,(20.0,20.0,0))
    set_pos(sta2,(10.0,20.0,0))
    set_pos(sta3,(20.0,10.0,0))
    set_pos(sta4,(10.0,10.0,0))
    set_pos(sta5,(30.0,30.0,0))
    set_pos(sta6,(30.0,10.0,0))
    set_pos(sta7,(10.0,30.0,0))
    set_pos(sta8,(20.0,30.0,0))
    set_pos(sta9,(30.0,20.0,0))

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()

    info("*** Replaying Mobility\n")
    ReplayingMobility(net)

    app = create_app(net)
    thread = threading.Thread(target=app.run)
    thread.daemon = True
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # do not flush the infinity of Flask messages to stdout
    thread.start()
    info("*** Initiated HTTP server for changing directions of drones on request")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


def set_pos(sta,start_pos):
    sta.p = []
    actual_pos = list(start_pos)
    pos = (-1000, 0, 0)
    sta.position = pos
    for _ in range(10000):
        sta.p.append(tuple(actual_pos))
    


if __name__ == '__main__':
    setLogLevel('info')

    topology()

