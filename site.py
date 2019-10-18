import socket
import sys
import os
import pickle


# Loads an pickled data from dict.log into a list
def load_log():
    if not os.path.exists('dict.log'):
        return []
    l = []
    with open('dict.log', 'rb') as log: # append to the log
        while(True):
            try:
                r = pickle.load(log)
                l.append(r)
            except EOFError:
                break
        return l


class site(object):
    def __init__(self, N, site_id):
        self.time = [[0]*N]*N # matrix clock of N sites
        self.id = site_id 
        self.p = 0 # TODO: figure out way to have a process id
        self.d = load_log()
    # Getter for log in RAM
    def __getitem__(self, arg):
        return self.d[arg]
    # Logs an item (client_name, list_of_flight_numbers, status)
    def add(self, item):
        print(self.time)
        self.time[self.p][self.p] += 1
        print(self.time)
        with open('dict.log', 'ab') as log: # append to the log
            eventR = (item, self.time, 'add')
            pickle.dump(eventR, log) # put the event record in stable storage
            self.d.append(eventR)
    # Takes a username and adds a delete event to the log
    def delete(self, item):
        self.time[self.p][self.p] += 1
        with open('dict.log', 'ab') as log:
            eventR = (item, self.time, 'delete')
            pickle.dump(eventR, log)
            self.d.append(eventR)


# Set port and IP address for server
IP = '127.0.0.1'
PORT = 8080

# Make socket and bind address and port to it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servaddr = (IP, PORT)
sock.bind(servaddr)

# Create log based dict
log = site(3, 0)

if __name__ == '__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*servaddr))
    while(True):
        #data, addr = sock.recvfrom(1024) # 1024 is the buffer size
        #print('received {} bytes'.format(len(data)));

        if (sys.argv[1] == '0'):
            log.add(('John', [1234], 'pending'))
            log.add(('Hank', [1234], 'pending'))
            log.add(('Arin', [1234], 'pending'))
            log.add(('Danny', [1234], 'pending'))
            #log.delete('Bob')

        print(log.d)

        # Take User Input
        #command = input()
        #if 'reserve' in command:
        #    pass
        #if 'cancel' in command:
        #    pass
        #if 'view' in command:
        #    pass

        break
