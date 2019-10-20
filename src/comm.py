import socket
import select
import json

from DSAsite import *

# TODO: make dictinary of other sites and their IP addresses and Ports
with open('knownhosts.json', 'r') as knownhosts:
    site_dict = json.load(knownhosts)['hosts']
    for i, host in enumerate(sorted(site_dict.keys())):
        site_dict[host]['pid'] = i

# Set port and IP address for local site
site_name = sys.argv[1]
IP = site_dict[site_name]['ip_address']
PORT = site_dict[site_name]['udp_start_port']

# Make socket and bind address and port to it
site_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
siteaddr = (IP, PORT)
site_sock.bind(siteaddr)

if __name__ == '__main__':
    #print('Starting server at IP: {} and PORT: {}'.format(*siteaddr))
    site = Site(len(site_dict), site_name, site_dict[site_name]['pid'])
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
            command, *args = command.split()
        if msg is not None:
            NPk, Tk = pickle.loads(msg)
            site.update_dict(NPk)
            site.update_matrix_clock(Tk, 0)
            site.truncate()
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
            # TODO: Look up port and address
            msg = pickle.dumps((site.get_partial_log(1), site.time))
            site_sock.sendto(msg, siteaddr)
        elif command == 'quit': # command is quit
            break

