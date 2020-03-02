import pickle

from Ingredients import *
from meal import *
from order import *
from request import *
import socket
import sys

HEADERSIZE = sys.getsizeof(int)
PORT = 3000
SIZE = 4096
HOST = '127.0.0.1'
soc = None
ing_map = None


def connect_to_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    global soc
    soc = s


def send_object(data):
    if soc is None:
        raise NotImplementedError  # There is no connection
    else:
        # make data as bytes
        msg = pickle.dumps(data)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
        soc.send(msg)


def get_object(req):
    global soc
    if soc is None:
        raise NotImplementedError  # There is no connection
    else:
        send_object(req)
        # unpickle the data
        length = soc.recv(HEADERSIZE).decode('utf-8')
        if len(length):
            length = int(length)
            data = b''
            while True:
                part = soc.recv(min(SIZE, length - len(data)))
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


def send_order(order):
    if order is not None:
        send_object(Soc_request(Request.P_ORDER, order))


def main():

    global ing_map
    connect_to_client()
    print('send ', sys.getsizeof(Soc_request(Request.G_ING_MAP, None)))
    ing_map = get_object(Soc_request(Request.G_ING_MAP, None))

    #send order
    burger = Burger(ing_map)
    salad = Salad(ing_map)
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
    send_order(o1)
    send_order(o2)
    send_order(o3)
    send_order(o4)
    send_order(o5)
    send_order(o6)


    soc.close()


if __name__ == "__main__":
    main()
