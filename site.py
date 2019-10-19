import socket
import sys
import os
import pickle


# Loads an pickled data from dict.log into a list
def load_log():
    l = []
    if os.path.exists('dict.log'):
        with open('dict.log', 'rb') as log: # append to the log
            while(True):
                try:
                    er = pickle.load(log)
                    l.append(er)
                except EOFError:
                    break
    return l


class eventR(object):
    def __init__(self, op, name, flights, time, node):
        self.op = op
        self.name = name
        self.flights = flights
        self.time = time
        self.node = node
    def __repr__(self):
        op = self.op
        name = self.name
        if (op == 'insert'):
            flights = ','.join(self.flights)
            return '{} {} {}'.format(op, name, flights)
        if (op == 'delete'):
            return '{} {}'.format(op, name)
        return 'unknown event'


class Distributed_Dictionary(object):
    def __init__(self, N, site_id):
        self.time = [[0]*N]*N # matrix clock of N sites
        self.id = site_id 
        self.p = 0 # TODO: figure out way to have a process id
        self.dict = {}
    # Getter for log in RAM
    def __getitem__(self, arg):
        return self.dict[arg]
    # Logs an item (client_name, list_of_flight_numbers)
    def insert(self, name, flights, rebuild=False):
        self.time[self.p][self.p] += 1
        with open('dict.log', 'ab') as log: # append to the log
            er = eventR('insert', name, flights, self.time, self.p)
            self.dict[name] = [flights, 'pending']
            if not rebuild:
                pickle.dump(er, log) # put the event record in stable storage
    # Takes a username and adds a delete event to the log
    def delete(self, name, rebuild=False):
        if name not in self.dict:
            return
        self.time[self.p][self.p] += 1
        with open('dict.log', 'ab') as log:
            er = eventR('delete', name, None, self.time, self.p)
            self.dict.pop(name)
            if not rebuild:
                pickle.dump(er, log)
    # When we know every other process know of an event, truncate the log
    def truncate(self):
        pass
    # View the contents of the log
    def view_log(self):
        log = load_log()
        for er in log:
            print(er)
    # View the contents of the dictionary
    def view(self):
        pass
        


# Set port and IP address for server
IP = '127.0.0.1'
PORT = 8080

# Make socket and bind address and port to it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servaddr = (IP, PORT)
sock.bind(servaddr)

# Create log based dict
dist_dict = Distributed_Dictionary(3, 0)

if __name__ == '__main__':
    print('Starting server at IP: {} and PORT: {}'.format(*servaddr))
    # Restore log if the site crashed
    log = load_log()
    for er in log:
        if (er.op == 'insert'):
            dist_dict.insert(er.name, er.flights, rebuild=True)
        if (er.op == 'delete'):
            dist_dict.delete(er.name, rebuild=True)

    while(True):
        #data, addr = sock.recvfrom(1024) # 1024 is the buffer size
        #print('received {} bytes'.format(len(data)));

        if (sys.argv[1] == '0'):
            dist_dict.insert('Arin',  ['1','2'])
            dist_dict.insert('Dan',  ['3'])
            dist_dict.delete('Arin')

        dist_dict.view_log()
        

        # Take User Input
        #command = input()
        #if 'reserve' in command:
        #    pass
        #if 'cancel' in command:
        #    pass
        #if 'view' in command:
        #    pass

        break
