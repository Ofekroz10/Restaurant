import json
import pickle

from Ingredients import *
from meal import *
from order import *
import socket
from request import *
from kitchen import *

HOST = '127.0.0.1'
PORT = 3000
SIZE = 1000
HEADERSIZE = 10
WORKERS = 2

conn = None
addr = None
soc = None
order_m = None


def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    global conn, addr
    global soc
    soc = s
    conn, addr = s.accept()


def send_object(data):
    if soc is None:
        raise NotImplementedError  # There is no connection
    else:
        # make data as bytes
        global conn
        msg = pickle.dumps(data)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
        conn.send(msg)


def get_object():
    global conn
    if conn is None:
        raise NotImplementedError  # There is no connection
    else:
        # unpickle the data
        data = b''
        while True:
            part = conn.recv(SIZE)
            data += part
            if len(part) < SIZE:
                break
        full_msg = data
        try:
            data = pickle.loads(full_msg[HEADERSIZE:])
        except EOFError:
            data = None
        return data


def main():
    create_connection()
    # Initialize objects
    global order_m
    ing_map = Ingredient_map()
    order_m = OrderManager()
    kitchen_obj = Kitchen(WORKERS)

    while True:
        msg = get_object()
        if msg is None:
            pass
        elif msg.req == Request.G_ING_MAP:  # get ingredient map
            send_object(ing_map.instance.map)
        elif msg.req == Request.P_ORDER:
            order_m.add_order(msg.data)
            print(msg.data)

    # end while
    soc.close()


if __name__ == "__main__":
    main()
