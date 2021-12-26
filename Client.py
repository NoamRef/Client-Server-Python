import socket
import sys
from struct import *
from socket import *
from select import select

#Consts
TIME_OUT = 10
UDP_PORT = 13118
BUFFER_SIZE = 1024
COOKIE = 0xabcddcba
MSG_TYPE = 0x2
TEAM_NAME = "Dothraki"

#colors for fun
BOLD = '\033[1m'
RED = '\033[91m'
HEADER = '\033[95m'


def mainF():
    UDPclient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) # UDP
    UDPclient.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    UDPclient.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    UDPclient.bind(("", UDP_PORT))
    while True: # serching for connections
        print("Client started, listening for offer requests...")
        data, addr = UDPclient.recvfrom(BUFFER_SIZE)
        try:
            cookie, msg_type, tcp_port = unpack('LBH',data)
            if(cookie != COOKIE or msg_type != MSG_TYPE):
                raise "m"
            print(BOLD+"Received offer from {0}, attempting to connect...".format(addr[0]))
            TCPclient = socket(AF_INET, SOCK_STREAM) # create tcp socket
            toConnectTo = (addr[0],tcp_port)
            TCPclient.connect(toConnectTo)
            TCPclient.send(TEAM_NAME.encode()) # sends team name over tcp
            msg = TCPclient.recv(BUFFER_SIZE).decode() # get message from server + question
            print(msg)
            game(TCPclient)

        except error:
            print(RED+"socket error, searching for another connection\n\n"+HEADER)

        except:
            print("Message is not supported ! ")



def game(TCPsocket):
    try:
        reads, out, e = select([sys.stdin, TCPsocket], [], [], TIME_OUT) # waits timeout time for input from the client
        if(sys.stdin in reads):
        # Means we got input from stdin, we should write it to the socket
            answer = sys.stdin.readline().encode()
            TCPsocket.send(answer) # sends answer
            print("asnwer sent")
            response = TCPsocket.recv(BUFFER_SIZE).decode() # get final message from the server
            print("got response")
            print(response)
    except:
        TCPsocket.close()
        print(RED+"Something went wrong in the answerQuestion method")

if __name__ == "__main__":
    mainF()