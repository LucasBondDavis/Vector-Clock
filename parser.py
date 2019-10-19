import instruction as INS

class parser(object):
    def __init__(self, debug):
        #self.file_name = filename
        #self.fp = open(filename, 'r')
        self.is_debugging = debug
    #def close_file(self):
        #self.fp.close()
    #def open_file(self):
    
    def parse_line( self, string_line ):
        words = string_line.split() # take white space as default? yes.
        #print(words)
        #default parameters
        clientName = ''
        siteId = ''
        flightListInt = []
        
        #if the instruction is reserve
        if words[0] == 'reserve':
            #1st, get flight list
            flightListStr = words.pop().split(',')
            flightListInt = []
            for str in flightListStr:
                flightListInt += [int(str)] # same as append() here?
            #2nd, get client name
            clientName = words.pop()
            
            if self.is_debugging:
                print(flightListInt)
                print(flightListInt)
                print('client name: ' + clientName)
            #3rd, construct instruction and return it.
            instructionRe = INS.instruction('reserve', clientName, flightListInt, siteId)
            return instructionRe
        
        #if the instruction is cancel:
        elif words[0] == 'cancel':
            clientName = words.pop()
            if self.is_debugging:
                print('cancel ' + clientName)
            return INS.instruction('cancel', clientName, flightListInt, siteId)
        
        #if the instruction is view
        elif words[0] == 'view':
            if self.is_debugging:
                print('view')
            return INS.instruction('view', clientName, flightListInt, siteId)
        #if the instruction is log
        elif words[0] == 'log':
            if self.is_debugging:
                print('log')
            return INS.instruction('log', clientName, flightListInt, siteId)
        #if the instruction is sendall
        elif words[0] == 'sendall':
            if self.is_debugging:
                print('sendall')
            return INS.instruction('sendall', clientName, flightListInt, siteId)
        #if the instruction is clock:
        elif words[0] == 'clock':
            if self.is_debugging:
                print('clock')
            return INS.instruction('clock', clientName, flightListInt, siteId)
        #if the instruction is send
        elif words[0] == 'send':
            siteId = words.pop()
            if self.is_debugging:
                print('send ' + siteId)
            return INS.instruction('send', clientName, flightListInt, siteId)
        #else the instruction is quit
        else:
            if self.is_debugging:
                print('quit')
            return INS.instruction('quit', clientName, flightListInt, siteId)
        
        #TO DO: add method to continue reading a file and return a list of instructions?
        
if __name__ == '__main__':
    ps = parser( True) # file name doesn't matter in this test case.
    ps.parse_line('reserve Taz 1,2')
    ps.parse_line('cancel Tazasdfasdfa')
    ps.parse_line('send banana')
    ps.parse_line('quit')