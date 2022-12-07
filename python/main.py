import random
import socket
from TextBites import text2chunk, chunks2text
from binascii import unhexlify

# Fixed Length Header
FORMAT = 'utf-8'
HEADER_SIZE = 8
PRIME = 98561123
ROOT = 452
PORT = 1812
IP_ADDRESS = "138.9.175.1"


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
    # print(type(socket.gethostname()))
    # print(socket.gethostname())
    # s.bind((socket.gethostname(), PORT))
    s.bind(("10.15.135.51", PORT))
    s.listen()
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # Client Socket
    # send_msg(clientsocket, "Hello Client!")
    receive_msg(clientsocket)


def client_tcp():
    print("You are a client")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((socket.gethostname(), PORT))
    s.connect(("138.9.175.10", PORT))

    # first receive msg catches empty message from server
    # receive_msg(s)
    send_msg(s, "Hello Host!")


def send_msg(s, msg):
    chunks = text2chunk(msg)
    # header = format(len(msg), '0' + str(HEADER_SIZE) + 'x')
    # print(f">Now sending message: {fullmsg}")
    # byteheader = bytes(header,FORMAT)
    # print(f"Sending Header: {byteheader}")
    # s.send(byteheader)

    for chunk in chunks:
        width = 64
        fmt = '%%0%dx' % (width // 4)
        bytemsg = unhexlify(fmt % chunk)
        print(f"Sending Chunk: {bytemsg}")
        s.send(bytemsg)


def receive_msg(s):
    print(">Now trying to receive a message:")
    fullmsg = []
    msg = s.recv(HEADER_SIZE)
    # print(f"> New message length: {msg}")
    if not msg:
        return fullmsg

    chunks = []

    print(msg)
    print(type(msg))
    msglen = int.from_bytes(msg, "little")
    print(f"> Message Length: {msglen}")
    for i in range(msglen):
        msg = s.recv(8)
        chunks.append(msg)
        fullmsg.append(msg.decode(FORMAT))
    msg = s.recv(msglen)
    fullmsg.append(msg.decode(FORMAT))

    print(fullmsg)
    print(chunks)
    return chunks


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