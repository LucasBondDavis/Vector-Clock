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
    def __init__(self, N, site_name, site_id):
        self.time = [[0]*N for _ in range(N)] # matrix clock of N sites
        self.name = site_name 
        self.id = site_id # TODO: figure out way to have a process id
        self.dict = {}
    # Put an item into the dictionary and log the operations
    def insert(self, name, flights, rebuild=False, recv=False):
        self.time[self.site_id][self.site_id] += 1
        #if not set(flights).isdisjoint( \ #TODO: ENABLE
        #        set([i for res in self.dict.values() for i in res.flights])):
        #    print('Cannot schedule reservation for {}.'.format(name))
        #    return
        with open('dict.log', 'ab') as log: # append to the log
            er = EventR('insert', name, flights, \
                    self.time[self.site_id][self.site_id], self.site_id)
            self.dict[name] = Reservation(flights)
            if not rebuild:
                pickle.dump(er, log) # put the event record in stable storage
                if not recv:
                    print('Reservation submitted for {}.'.format(name))
    # Takes a username and adds a delete event to the log
    def delete(self, name, rebuild=False, recv=False):
        if name not in self.dict:
            return
        self.time[self.site_id][self.site_id] += 1
        with open('dict.log', 'ab') as log:
            er = EventR('delete', name, None, \
                    self.time[self.site_id][self.site_id], self.site_id)
            self.dict.pop(name)
            if not rebuild:
                pickle.dump(er, log)
                if not recv:
                    print('Reservation for {} canceled.'.format(name))
    #part of the algorithm
    def hasRec(self, Ti, eR, k):
        return Ti[k][eR.node] >= eR.time
    #figure out what NP is when sending a message to another site
    def get_partial_log(self, target_site_id):
        NP = set()
        j = target_site_id
        Ti = self.time
        PLi = load_log()
        for eR in PLi:
            if self.hasRec(Ti, eR, j) == False:
                NP.add(eR)
        return NP
    # figure out what NE is after received a message, and calling receive().
    def update_dict(self, NP):
        NE = set()
        i = self.site_id
        Ti = self.time
        for fR in NP:
            if self.hasRec(Ti, fR, i) == False:
                NE.add(fR)
        for eR in list(NE):
            if eR.op == 'insert':
                #if eR.name in Vi and eR.time:
                #    print('overwriting an entry in dictionary')
                self.insert(eR.name, eR.flights, recv=True)
            if dR.op == 'delete': 
                self.delete(eR.name, recv=True)
    #update matrix clock.
    def update_matrix_clock(self, Tk, sender_site_id):
        k = sender_site_id
        Ti = self.time
        N = len(self.time)
        for r in range(N):
            Ti[self.site_id][r] = max(Ti[self.site_id][r], Tk[k][r] )
        for r in range(N):
            for s in range(N):
                Ti[r][s] = max( Ti[r][s], Tk[r][s] ) 
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
    def restore(self):
        # Restore log if the site crashed
        log = load_log()
        for er in log:
            if (er.op == 'insert'):
                self.insert(er.name, er.flights, rebuild=True)
            if (er.op == 'delete'):
                self.delete(er.name, rebuild=True)


if __name__ == '__main__':
    # Create log based dict
    dist_dict = Site(3, 'apple', 0)
    dist_dict.restore()

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

