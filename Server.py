from scapy.all import *
from struct import *
import socket
import time

tcpPort = 3200
enthrent = "eth1" # to chagne to eht2 in testing

myIp = get_if_addr(enthrent) # get my cp is
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # udp socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # enables more clients
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # enable bordcast
message = pack('I',0xabcddcba) + pack('b',0x02) + pack('h',tcpPort)
print(message)
'''
print("Server started, listening in IP address " + myIp)
while True:
    server.sendto(message, ('<broadcast>', 13118)) ## udp port 13117
    print("message sent!")
    time.sleep(1)
'''

def handler(c):
    return