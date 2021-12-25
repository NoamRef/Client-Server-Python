import socket
from struct import *


UDPclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
UDPclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
UDPclient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
isConnected = False
UDPclient.bind(("", 13118))
print("Client started, listening for offer requests...")
while True:
    while (not isConnected): # serching for connections
        data, addr = UDPclient.recvfrom(1024)
        try:
            magicCookie = data.hex()[0:8] # validation sagment(depends on server encode !, hopes mine is allright)
            if (magicCookie != "abcddcba"):
                raise "cookie is bad"
            messageType = int("0x" + data.hex()[9:10],16)
            if (messageType != 2):
                raise "type is bad"
            tcpPort = int("0x" + data.hex()[-4:],16) # decode port from message (offer is accepted)


        except:
            print("Message is not supported ! ")
