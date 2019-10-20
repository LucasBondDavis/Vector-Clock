

def parse_line(string_line):
    command, args = string_line.split() # take white space as default? yes.
    
    #if the instruction is reserve
    if command[0] == 'reserve':
        #1st, get flight list
        flights = args.pop().split(',')
        #2nd, get client name
        clientName = args.pop()
        #3rd, construct instruction and return it.
        instructionRe = INS.instruction('reserve', clientName, flightListInt, siteId)
        return instructionRe
    #if the instruction is cancel:
    elif command == 'cancel':
        clientName = args.pop()
        return INS.instruction('cancel', clientName, flightListInt, siteId) 
    #if the instruction is view
    elif command == 'view':
        return INS.instruction('view', clientName, flightListInt, siteId)
    #if the instruction is log
    elif command == 'log':
        return INS.instruction('log', clientName, flightListInt, siteId)
    #if the instruction is sendall
    elif command == 'sendall':
        return INS.instruction('sendall', clientName, flightListInt, siteId)
    #if the instruction is clock:
    elif command == 'clock':
        return INS.instruction('clock', clientName, flightListInt, siteId)
    #if the instruction is send
    elif command == 'send':
        siteId = args.pop()
        return INS.instruction('send', clientName, flightListInt, siteId)
    #else the instruction is quit
    else:
        return INS.instruction('quit', clientName, flightListInt, siteId)
    
    #TO DO: add method to continue reading a file and return a list of instructions?
        
if __name__ == '__main__':
    parse_line('reserve Taz 1,2')
    parse_line('cancel Tazasdfasdfa')
    parse_line('send banana')
    parse_line('quit')
