import sys
import os
import pickle
from dataclasses import dataclass


# Loads a pickled event records from dict.log into a list
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


@dataclass
class Reservation:
    flights: list
    status: str = 'pending'

# A simple class to store event records
class EventR(object):
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


class Site(object):
    def __init__(self, N, site_id):
        self.time = [[0]*N for _ in range(N)] # matrix clock of N sites
        self.id = site_id 
        self.p = 0 # TODO: figure out way to have a process id
        self.dict = {}
    # Put an item into the dictionary and log the operations
    def insert(self, name, flights, rebuild=False):
        self.time[self.p][self.p] += 1
        if not set(flights).isdisjoint( \
                set([i for res in self.dict.values() for i in res.flights])):
            print('Cannot schedule reservation for {}.'.format(name))
            return
        with open('dict.log', 'ab') as log: # append to the log
            er = EventR('insert', name, flights, self.time, self.p)
            self.dict[name] = Reservation(flights)
            if not rebuild:
                pickle.dump(er, log) # put the event record in stable storage
        print('Reservation submitted for {}.'.format(name))
    # Takes a username and adds a delete event to the log
    def delete(self, name, rebuild=False):
        if name not in self.dict:
            return
        self.time[self.p][self.p] += 1
        with open('dict.log', 'ab') as log:
            er = EventR('delete', name, None, self.time, self.p)
            self.dict.pop(name)
            if not rebuild:
                pickle.dump(er, log)
    # When we know every other process know of an event, truncate the log
    def truncate(self):
        pass # TODO: implement this
    # View the contents of the log
    def print_log(self):
        log = load_log()
        for er in log:
            print(er)
    # View the contents of the dictionary
    def view(self):
        for name in sorted(self.dict.keys()):
            print('{} {} {}'.format(name, \
                    ','.join(self.dict[name].flights), \
                    self.dict[name].status))
    # Prints this site's matrix clock
    def clock(self):
        for i in range(len(self.time)):
            print(' '.join(str(j) for j in self.time[i]))
        


if __name__ == '__main__':
    # Create log based dict
    dist_dict = Site(3, 0)

    # Restore log if the site crashed
    log = load_log()
    for er in log:
        if (er.op == 'insert'):
            dist_dict.insert(er.name, er.flights, rebuild=True)
        if (er.op == 'delete'):
            dist_dict.delete(er.name, rebuild=True)

    #data, addr = sock.recvfrom(1024) # 1024 is the buffer size
    #print('received {} bytes'.format(len(data)));

    if (sys.argv[1] == '0'):
        dist_dict.insert('Dan',  ['3'])
        dist_dict.insert('Arin',  ['1','2'])
        dist_dict.insert('Hank', ['1'])
    if (sys.argv[1] == '1'):
        dist_dict.delete('Arin')

    print('log')
    dist_dict.print_log()
    print('view')
    dist_dict.view()
    print('clock')
    dist_dict.clock()

