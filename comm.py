import site
import socket


# Set port and IP address for server
IP = '127.0.0.1'
PORT = 8080

# Make socket and bind address and port to it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servaddr = (IP, PORT)
sock.bind(servaddr)

if __name__=='__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*servaddr))
