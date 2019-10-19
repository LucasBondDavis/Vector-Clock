class reservation(object):
    def __init__(self):
        self.client_name_ = ""
        self.list_of_flight_numbers_ = None
        self.status_pending = True #status should be pending when application creates a local reservation