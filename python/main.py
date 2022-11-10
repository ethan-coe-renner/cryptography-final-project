import random
import socket
from math import floor

import TextBites
# Fixed Length Header
FORMAT = 'utf-8'
HEADER_SIZE = 4
PRIME = 98561123
ROOT = 452


def main():
    i = input("1: Host\n2:Client\n>")

    if i == '1':
        host_tcp()
    if i == '2':
        client_tcp()

    # Do cool chat stuff here
    return "meh"


def host_tcp():
    print("You are a host")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen()
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # Client Socket
    send_msg(clientsocket, "Hello Client!")
    receive_msg(clientsocket)


def client_tcp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))

    # first receive msg catches empty message from server
    receive_msg(s)
    send_msg(s, "Hello Host!")



def send_msg(s, msg):
    fullmsg = format(len(msg), '0' + str(HEADER_SIZE) + 'x') + msg
    # print(f"Now sending message: {fullmsg}")
    s.send(bytes(fullmsg, FORMAT))


def receive_msg(s):
    # print("Now trying to receive a message:")
    fullmsg = []
    msg = s.recv(HEADER_SIZE)
    # print(f"New message length: {msg}")
    if not msg:
        return fullmsg

    msglen = int(msg, base=16)
    # print(f"Message Length: {msglen}")
    #for i in range(msglen):
    #    msg = s.recv(8)
    #    fullmsg.append(msg.decode(FORMAT))
    msg = s.recv(msglen)
    fullmsg.append(msg.decode(FORMAT))

    print(fullmsg)
    return fullmsg


def diffie_hellman(prime, root):
    r = random.randint(2, prime - 2)
    a = pow(root, r, prime)

    # Networking, send 'a' to other computer, receive 'b' in return
    b = 0

    # 'k' is our key
    k = pow(b, r, prime)

    return k


if __name__ == "__main__":
    main()