from contextlib import nullcontext
from scapy.all import *
from struct import *
from socket import *
from select import select
from threading import Thread
import time
from random import random, randint

#colors for fun
BOLD = '\033[1m'
RED = '\033[91m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
RESET = "\x1b[0m"
GREEN = '\033[92m'
UNDERLINE = '\033[4m'

#consts
TIME_OUT = 10
BUFFER_SIZE = 1024
MSG_TYPE = 0x2
COOKIE = 0xabcddcba
TCP_PORT = randint(1500,55000)
UDP_PORT = 13117 # change to 13117
ETHERNET = "eth2" # to chagne to eht2 in testing

connected_clients = []

def mainF():
    myIp = get_if_addr(ETHERNET) # get my cp IP
    TCPserver = socket(AF_INET, SOCK_STREAM) # start tcp serer
    TCPserver.bind((myIp, TCP_PORT))
    TCPserver.listen(2) # waits for maximum 2 clients
    print(BOLD+BLUE+"Server started, listening in IP address " + myIp + RESET)

    while True:
        BrodcastThread = Thread(target = UDPBroadcast)
        BrodcastThread.start()
        TCPThread = Thread(target = TcpWelcoming,args=(TCPserver,))
        TCPThread.start()
        BrodcastThread.join()
        TCPThread.join() # we found 2 players
        print(BLUE+"Found 2 clients, Game is about to begin"+RESET)
        game()
        print(RED + "Game over, sending out offer requests..." + RESET)

def UDPBroadcast():
    UDPserver = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) # udp socket
    UDPserver.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1) # enables more clients
    UDPserver.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # enable broadcast
    message = pack('LBH',COOKIE,MSG_TYPE,TCP_PORT)
    myIp = get_if_addr(ETHERNET)[:-2]
    while(len(connected_clients) < 2):
        ip = str(myIp)
        for i in range(0,255): # brodcast
            ip = ip + str(i)
            UDPserver.sendto(message, (ip, UDP_PORT))
            ip = str(myIp)
        time.sleep(1)

def TcpWelcoming(TcpSocket):
    global connected_clients # allows to edit global vars
    while (len(connected_clients) < 2): # mroe clinents need to connect
        socket, addr = TcpSocket.accept() # waits
        connected_clients.append((socket, addr))

def game():
    global connected_clients
    socket1 = connected_clients[0][0]
    socket2 = connected_clients[1][0]
    try:
        team1 = PURPLE + socket1.recv(BUFFER_SIZE).decode() + RESET
        team2 = GREEN + socket2.recv(BUFFER_SIZE).decode() + RESET
        q, a , o = questionGenrator()
        message_to_send = UNDERLINE+"Welcome to quck Maths."+ RESET+"\nPlayer 1: "+ team1 + "\nplayer 2: " + team2 +"\n==\nPlease answer the following question as fast as you can\n" + BOLD + BLUE + "How much is " +  str(q[0]) + o + str(q[1]) + RESET + "?"
        time.sleep(TIME_OUT) # wait for start
        socket1.send(message_to_send.encode())
        socket2.send(message_to_send.encode())
        reads, out, e = select([socket1, socket2], [], [], TIME_OUT)
        teamToAnswer = ""
        teamTolose = ""
        answer = -1
        mssg = ""
        winnerTeam = ""
        if(len(reads) > 0): # timout didn't accure
            if(reads[0] == socket1):
                teamToAnswer = team1
                teamTolose = team2
                answer = socket1.recv(BUFFER_SIZE).decode()
            if(reads[0] == socket2):
                teamToAnswer = team2
                teamTolose = team1
                answer = socket2.recv(BUFFER_SIZE).decode()
            mssg = "!\nThe Team to answer was " + teamToAnswer+ " with the answer: " + answer
            answer = answer[0]
            if (str(a) == answer):
                winnerTeam = teamToAnswer
            else:
                winnerTeam = teamTolose
        message_to_send2 = RED +"\nGame over!" + RESET +"\nThe correct answer was " + BOLD + str(a) + mssg + RESET+ "\nCongratulations to the winner: \n" + winnerTeam + "\n"
        socket1.send(message_to_send2.encode())
        socket2.send(message_to_send2.encode())
        socket1.close()
        socket2.close()
        connected_clients = []
    except Exception as e:
        print(e)
        socket1.close()
        socket2.close()
        print (RED + BOLD + "Problem with connection" + RESET)
        connected_clients = []



def questionGenrator():
    operation = randint(0,1)
    number1 = randint(0,15)
    a= 0
    if(operation == 1 and number1 < 9): # '+'
        o = "+"
        number2 = randint(0,9-number1) 
        a = number1+number2
    else: # '-'
        o = "-"
        if(number1 <10):
            number2 = randint(0,number1)
        else:
            number2 = randint(number1-9,number1)
        a = number1-number2
    q = (number1,number2)
    return(q,a,o) # question,operation,answer

if __name__ == "__main__":
    mainF()
