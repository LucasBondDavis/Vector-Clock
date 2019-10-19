class instruction(object):
    def __init__(self, thisCommand, clientname, flightlist, siteid  ):
        self.command_ = thisCommand #string
        self.client_name_ = clientname # string, can be "" depends on the instruction
        self.flight_list = flightlist #list of integers, can be [] depends on the instruction
        self.site_id = siteid #string, can be "" depends on the instruction
        