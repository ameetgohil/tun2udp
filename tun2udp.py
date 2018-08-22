#! /usr/bin/env python

import os, sys
from socket import *
from fcntl import ioctl
from select import select
import struct
import subprocess
import time
import fcntl

TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0X0001
IFF_TAP = 0X0002
IFF_NO_PI = 0X1000

PORT = 1234

f = os.open("/dev/net/tun", os.O_RDWR)
#ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "tun2udp%d", TUNMODE))
#ifname = ifs[:16].strip("\x00")
ifr =  struct.pack('16sH', 'tun2udp0', IFF_TUN | IFF_NO_PI)
fcntl.ioctl(f, TUNSETIFF, ifr)
fcntl.ioctl(f, TUNSETOWNER, 1000)

subprocess.call('ip link set dev tun2udp' + str(0) + ' up', shell=True)
subprocess.call('ip addr add 10.0.0.2/24 dev tun2udp' + str(0), shell=True)

subprocess.call('ip route add default via 10.0.0.2', shell=True)

s = socket(AF_INET, SOCK_DGRAM)
#s.bind(("", PORT))

s_rx = socket(AF_INET, SOCK_DGRAM)
s_rx.bind(('192.168.1.69', 1235))

while 1:
    r = select([f,s_rx],[],[])[0][0]
    if r == f:
        message = os.read(f,1500)
#        os.write(1,message)
        s.sendto(message,('192.168.1.87', 1234))
#        print "r"
    else:
        buf,p = s_rx.recvfrom(1500)
        os.write(f,buf)
#        print "s_rx"

time.sleep(100)
