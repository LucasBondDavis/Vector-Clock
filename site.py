import socket
import sys
import pickle

class site(object):
    def __init__(self, N, site_id):
        self.time = [[]*N]*N # matrix clock of N sites
        self.id = site_id 
        self.p = 0 # TODO: figure out way to have a process id
        self.d = [] # dict: {(client_name, list_of_flight_numbers, status)}
    def __getitem__(self, arg):
        return 
    # TODO: change item to an event record with operation and timestamp
    def add(self, item):
        self.time[self.p][self.p] += 1
        with open('dict.log', ab) as log: # append to the log
            pickle.dump(item, log) # put the item in stable storage
    def delete(self, item):
        self.time[self.p][self.p] += 1
        with open('dict.log', ab) as log: # append to the log
            pickle.dump(item, log)


# Set global vars for server
IP = '127.0.0.1'
PORT = 8080

# Make socket and bind address and port to it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servaddr = (IP, PORT)
sock.bind(servaddr)

# Create log based dict
log = site(3, sys.argv[1])

if __name__ == '__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*servaddr))
    while(True):
        #data, addr = sock.recvfrom(1024) # 1024 is the buffer size
        #print('received {} bytes'.format(len(data)));
        
        break
