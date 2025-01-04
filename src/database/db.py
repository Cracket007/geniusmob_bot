from datetime import datetime

class RepairRequest:
    def __init__(self):
        self.phone_model = None
        self.problem = None
        self.contact = None
        self.timestamp = None

repair_requests = {} 