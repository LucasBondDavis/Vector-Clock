class message(object):
    def __init__(self, NP, Ti):
        self.log_entires = copy.copy(NP) # shallow copy should be ok?
        self.matrix_clock = copy.copy(Ti) # 
        