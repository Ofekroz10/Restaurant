import json
import pickle

from Ingredients import *
from exceptions import *
from meal import *
from order import OrderManager
import socket
import sys
from request import *
from kitchen import *


def synchronized(func):
    """ Represent synchronized keyword in java """
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class Server:
    HOST = '127.0.0.1'
    PORT = 3000
    SIZE = 1000
    HEADERSIZE = sys.getsizeof(int)
    WORKERS = 1
    _s_instance = None


    def __init__(self):
        self.conn = None
        self.addr = None
        self.soc = None
        self.order_m = None
        self.kitchen_obj = None
        self.ing_map = None
        self._next_order_id = 0
        self.meal_map = Ingredient_map.get_meals_map()
        print(self.meal_map)

    @synchronized
    def get_order_id(self):
        x = self._next_order_id
        self._next_order_id += 1
        return x

    @synchronized
    def __new__(cls, *args, **kwargs):
        if not cls._s_instance:
            cls._s_instance = super(Server, cls).__new__(cls, *args, **kwargs)
        return cls._s_instance

    def create_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen()
        self.soc = s
        self.conn, self.addr = s.accept()


    def send_object(self, data):
        if self.soc is None:
            raise NotImplementedError  # There is no connection
        else:
            # make data as bytes
            msg = pickle.dumps(data)
            msg = bytes(f"{len(msg):<{self.HEADERSIZE}}", 'utf-8') + msg
            self.conn.send(msg)

    def get_object(self):
        if self.conn is None:
            raise NotImplementedError  # There is no connection
        else:
            # unpickle the data
            length = self.conn.recv(self.HEADERSIZE).decode('utf-8')
            if len(length):
                length = int(length)
                data = b''
                while True:
                    part = self.conn.recv(min(self.SIZE, length - len(data)))
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

    @synchronized
    def prepare_order(self):
        order = None
        print(self.order_m)
        try:
            order = self.order_m.peek()
        except NotAvailableOrder:
            return

        try:
            self.kitchen_obj.make_order(order)
        except NotAvailableWorker:
            return

    def main(self):
        self.create_connection()
        # Initialize objects
        self.ing_map = Ingredient_map()
        self.order_m = OrderManager()
        self.kitchen_obj = Kitchen(self.WORKERS, self)

        while True:
            msg = self.get_object()
            if msg is None:
                pass
            elif msg.req == Request.G_ING_MAP:  # get ingredient map
                self.send_object(self.ing_map.instance.map)
            elif msg.req == Request.G_MEALS_MAP:
                self.send_object(self.meal_map)
            elif msg.req == Request.P_ORDER:
                x = self.get_order_id()
                msg.data.order_id = x
                self.order_m.add_order(msg.data)
                self.prepare_order()
                self.send_object(x)

        # end while
        soc.close()


if __name__ == "__main__":
    server = Server()
    server.main()
