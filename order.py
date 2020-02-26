from enum import IntEnum
from _collections import  deque


class Priority(IntEnum):
    NORMAL = 0
    PLUS = 1
    VIP = 2


class Order:
    """ represent an order, id is class variable """
    id = 0

    def __init__(self, priority, ):
        self.meals_lst = list()
        self.order_id = Order.id
        Order.id = Order.id+1
        self.priority = priority

    def __str__(self):
        return str(self.order_id) + ' ' + str(self.priority)


class Priorityble:
    def __init__(self, priority):
        self._priority = priority

    @property
    def priority(self):
        try:
            return  self._priority
        except:
            raise NotImplementedError


class Client(Priorityble):
    def __init__(self,name,priority):
        super(priority)
        self.name = name


class OrderManager:
    def __init__(self):
        self._orders = PriorityQueue()

    def add_order(self, order):
        self._orders.append(order)

    def pop_order(self, order):
        return self._orders.pop()

    def peek(self):
        return self._orders.peek()

    def __str__(self):
        return str(self._orders)

    def __len__(self):
        return len(self._orders)


class PriorityQueue:
    def __init__(self):
        self.collection = deque()

    def __str__(self):
        return ' '.join([str(i) for i in self.collection])

    def append(self, order):
        if len(self.collection) == 0:
            self.collection.append(order)
        else:
            i = 0
            for item in self.collection:
                if item.priority >= order.priority:
                    i = i+1
                else:
                    break
            self.collection.insert(i, order)

    def pop(self):
        self.collection.pop()

    def peek(self):
        return self.collection[0]

    def __len__(self):
        return len(self.collection)



