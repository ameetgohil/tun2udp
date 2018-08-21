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
subprocess.call('ip addr add 10.0.0.1/24 dev tun2udp' + str(0), shell=True)

s = socket(AF_INET, SOCK_DGRAM)
#s.bind(("", PORT))


while 1:
    r = select([f,s],[],[])[0][0]
    if r == f:
        message = os.read(f,1500)
        os.write(1,message)
        s.sendto(message,('127.0.0.1', 1234))

        

time.sleep(100)
