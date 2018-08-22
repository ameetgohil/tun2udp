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
UDP_SERVER_IP = '192.168.1.69'

PORT = 1234
f = os.open("/dev/net/tun", os.O_RDWR)
#ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "tun2udp%d", TUNMODE))
#ifname = ifs[:16].strip("\x00")
ifr =  struct.pack('16sH', 'tun2udp0', IFF_TUN | IFF_NO_PI)
fcntl.ioctl(f, TUNSETIFF, ifr)
fcntl.ioctl(f, TUNSETOWNER, 1000) 

subprocess.call('ip link set dev tun2udp' + str(0) + ' up', shell=True)
subprocess.call('ip addr add 10.0.0.1/24 dev tun2udp' + str(0), shell=True)
subprocess.call('sysctl -w net.ipv4.ip_forward=1', shell=True)
subprocess.call('iptables -t nat --flush')
subprocess.call('iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE', shell=True)


s = socket(AF_INET, SOCK_DGRAM)
s.bind(('192.168.0.24', PORT))


while 1:
    r = select([f,s],[],[])[0][0]
    if r==s:
        buf,p = s.recvfrom(1500)
        #buf = buf[:15] + '\x04' + buf[16:]

        #   print buf.encode("hex")
        os.write(f,buf)
        icmp_req = b'E\x00\x00(\x00\x00\x00\x00@\x01`\xc2\n\x00\x00\x01\x08\x08'\
               '\x08\x08\x08\x00\x0f\xaa\x00{\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00test'
        icmp_req = icmp_req[:15] + '\x04' + icmp_req[16:]
        #    buf = buf[:0x18] + icmp_req[0x18] + icmp_req[0x19] + buf[20:]
        #    print icmp_req.encode("hex")
        #    os.write(f, icmp_req)
#    else:
        

time.sleep(100)
