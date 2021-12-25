from scapy.all import *
from struct import *
from socket import *
from select import select
from threading import Thread
import time

#colors for fun
RED = '\033[91m'
BOLD = '\033[1m'

#consts
TIME_OUT = 10
BUFFER_SIZE = 1024
MSG_TYPE = 0x2
COOKIE = 0xabcddcba
TCP_PORT = 3200
UDP_PORT = 13118
ETHERNET = "eth1" # to chagne to eht2 in testing

connected_clients = []

def main():
    myIp = get_if_addr(ETHERNET) # get my cp IP
    TCPserver = socket(AF_INET, SOCK_STREAM) # start tcp serer
    TCPserver.bind(('', TCP_PORT))
    TCPserver.listen(2) # waits for maximum 2 clients
    print(BOLD+"Server started, listening in IP address " + myIp)

    print("Server started, listening in IP address " + myIp)
    while True:
        BrodcastThread = Thread(UDPBroadcast())
        BrodcastThread.start()
        TCPThread = Thread(TcpWelcoming(TCPserver))
        TCPThread.start()
        BrodcastThread.join()
        TCPThread.join() # we found 2 players
        game()

def UDPBroadcast():
    UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # udp socket
    UDPserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # enables more clients
    UDPserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # enable broadcast
    message = pack('LBH',COOKIE,MSG_TYPE,TCP_PORT)
    while(len(connected_clients)) != 2:
        UDPserver.sendto(message, ('<broadcast>', UDP_PORT)) # udp port 13117
        print("broadcast sent!")
        time.sleep(1)

def TcpWelcoming(TcpSocket):
    global connected_clients # allows to edit global vars
    while len(connected_clients) != 2: # mroe clinents need to connect
        socket, addr = TcpSocket.accept() # waits
        connected_clients.append((socket, addr))

def game():
    

main()