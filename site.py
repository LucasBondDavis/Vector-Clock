import socket
import sys

IP = '127.0.0.1'
PORT = 8080
msg = 'Hello World'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

servaddr = (IP, PORT)
sock.bind(servaddr)

if __name__ == '__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*servaddr))
    while(True):
        data, addr = sock.recvfrom(1024) # 1024 is the buffer size
        print('received {] bytes'.format(len(data)));
        print(data)
        break
