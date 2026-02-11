from enum import Enum

class Status(Enum):
    AWAITING_DATA = 0
    PROCESSING = 1
    READY = 2

class ServerState:
    def __init__(self):
        self.status = Status.AWAITING_DATA
        self.rag_model = None


state = ServerState()