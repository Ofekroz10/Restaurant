import pickle

from Ingredients import *
from meal import *
from request import *
import socket
import sys
from order import *
import ClientGUI
import globals

HEADERSIZE = sys.getsizeof(int)
PORT = 3000
SIZE = 4096
HOST = '127.0.0.1'


class Client:

    def __init__(self):
        self.soc = None

    def connect_to_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        self.soc = s

    def send_object(self, data):
        if self.soc is None:
            raise NotImplementedError  # There is no connection
        else:
            # make data as bytes
            msg = pickle.dumps(data)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
            self.soc.send(msg)

    def get_object(self, req=None, flag=False):
        if self.soc is None:
            raise NotImplementedError  # There is no connection
        else:
            if not flag:
                self.send_object(req)
            # unpickle the data
            length = self.soc.recv(HEADERSIZE).decode('utf-8')
            if len(length):
                length = int(length)
                data = b''
                while True:
                    part = self.soc.recv(min(SIZE, length - len(data)))
                    data += part
                    if length == len(data):
                        break
                full_msg = data
                try:
                    data = pickle.loads(full_msg)
                except EOFError:
                    data = None
                return data
            else:
                return None

    def send_order(self, order):
        if order is not None:
            self.send_object(Soc_request(Request.P_ORDER, order))
            x = self.get_object(flag=True)
            return x

    def example(self):
        # send order
        """"
        burger = Burger(globals.ing_map, globals.meals_map)
        salad = Salad(globals.ing_map, globals.meals_map)
        burger.add_ingredient('ham')
        o1 = Order(Priority.NORMAL)
        o2 = Order(Priority.NORMAL)
        o3 = Order(Priority.VIP)
        o4 = Order(Priority.VIP)
        o5 = Order(Priority.PLUS)
        o6 = Order(Priority.PLUS)
        o1.meals_lst.append(burger)
        o3.meals_lst.append(burger)
        o2.meals_lst.append(burger)
        o4.meals_lst.append(burger)
        o5.meals_lst.append(burger)
        o6.meals_lst.append(burger)
        self.send_order(o1)
        self.send_order(o2)
        self.send_order(o3)
        self.send_order(o4)
        self.send_order(o5)
        self.send_order(o6)
        """

    def main(self):
        self.connect_to_client()
        globals.ing_map = self.get_object(Soc_request(Request.G_ING_MAP, None))
        globals.meals_map = self.get_object(Soc_request(Request.G_MEALS_MAP, None))
        print(globals.ing_map)
        ClientGUI.show(self)


if __name__ == "__main__":
    client = Client()
    client.main()
