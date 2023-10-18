#!/usr/bin/python

'Replaying Mobility'

import os
import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.replaying import ReplayingMobility
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02',
                          ip='10.0.0.1/8', speed=1)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03',
                          ip='10.0.0.2/8', speed=1)
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04',
                          ip='10.0.0.3/8', speed=1)
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05',
                          ip='10.0.0.4/8', speed=1)
    #ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
    #                         position='45,45,0')
    #c1 = net.addController('c1', controller=Controller)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Creating links\n")
    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0', ssid='adhocNet')
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0', ssid='adhocNet')
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0', ssid='adhocNet')
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0', ssid='adhocNet')

    net.isReplaying = True
    get_trace(sta1,(20.0,20.0,0),(40.0,20.0,0),(40.0,40.0,0))
    get_trace(sta2,(10.0,20.0,0),(30.0,20.0,0),(30.0,40.0,0))
    get_trace(sta3,(20.0,10.0,0),(40.0,10.0,0),(40.0,30.0,0) )
    get_trace(sta4,(10.0,10.0,0),(30.0,10.0,0),(30.0,30.0,0))

    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    #c1.start()
    #ap1.start([c1])

    info("*** Replaying Mobility\n")
    ReplayingMobility(net)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


def get_trace(sta,start_pos, midle_pos, final_pos):
    sta.p = []
    actual_pos = list(start_pos)
    pos = (-1000, 0, 0)
    sta.position = pos

    sta.p.append(tuple(actual_pos))
    for data in range(10):
        vel_x = (midle_pos[0] - start_pos[0])/10
        vel_y = (midle_pos[1] - start_pos[1])/10
        actual_pos[0] += vel_x
        actual_pos[1] += vel_y
        actual_pos[2] = 0.0
        sta.p.append(tuple(actual_pos))
        
    actual_pos=list(midle_pos)
    
    for data in range(20):
        sta.p.append(midle_pos)
    
    for data in range(10):
        vel_x = (final_pos[0] - midle_pos[0])/10
        vel_y = (final_pos[1] - midle_pos[1])/10
        actual_pos[0] += vel_x
        actual_pos[1] += vel_y
        actual_pos[2] = 0.0
        sta.p.append(tuple(actual_pos))


if __name__ == '__main__':
    setLogLevel('info')
    topology()
