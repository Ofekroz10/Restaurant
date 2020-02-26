from enum import Enum


class Request(Enum):
    G_ING_MAP = 0
    P_ORDER = 1


class Soc_request:
    def __init__(self,req,data):
        self.req = req
        self.data = data