import socket
import select

from Site import *


# TODO: make dictinary of other sites and their IP addresses and Ports
# Set port and IP address for local site
IP = '127.0.0.1'
PORT = 8080

# Make socket and bind address and port to it
site_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
siteaddr = (IP, PORT)
site_sock.bind(siteaddr)

if __name__ == '__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*siteaddr))
    site = Site(2, 0)
    site.restore()
    while(True):
        socket_list = [sys.stdin, site_sock]
        r_socks, _, _ = select.select(socket_list, [], [])
        command = None
        msg = None
        for sock in r_socks:
            if sock is site_sock: # recv message from another site
                msg, addr = sock.recvfrom(1024) # 1024 char buffer size
            else:
                command = input()

        if command is not None:
            command, *args = user_input.split()
        if msg is not None:
            pass
        if command == 'reserve':
            flights = args.pop().split(',')
            clientName = args.pop()
            site.insert(clientName, flights)
        elif command == 'cancel':
            clientName = args.pop()
            site.delete(clientName)
        elif command == 'view':
            site.view()
        elif command == 'log':
            site.print_log()
        elif command == 'sendall':
            pass
        elif command == 'clock':
            site.clock()
        elif command == 'send':
            siteId = args.pop()
            # LOOK up port and address
        else: # command is quit
            break

