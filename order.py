
import sys
from enum import IntEnum
from heapq import *
import exceptions


class Priority(IntEnum):
    NORMAL = 2
    PLUS = 1
    VIP = 0


class Order:
    """ represent an order, id is class variable """
    id = 0

    def __init__(self, priority, ):
        self.meals_lst = list()
        self.order_id = Order.id
        Order.id = Order.id + 1
        self.priority = priority

    def __str__(self):
        return str(self.order_id) + ' ' + str(self.priority)

    def calc_sec(self):
        sec = 0
        for meal in self.meals_lst:
            sec += meal.seconds
        return sec


class OrderManager:  # make singlethon... with thread safe
    def __init__(self):
        self._orders = PriorityQueue(self)
        self.map = {}

    def add_order(self, order):
        id = order.order_id
        self.map[id] = order
        self._orders.append(id)
        print('add order ', id, ' to the queue')

    def pop_order(self):
        if len(self._orders) == 0:
            raise exceptions.NotAvailableOrder
        return self._orders.pop()

    def peek(self):
        return self._orders.peek()

    def __str__(self):
        return '$ ' + str(self._orders)

    def __len__(self):
        return len(self._orders)


class PriorityQueue:
    def __init__(self, order_manager):
        self.collection = []
        self.order_manager = order_manager

    def __str__(self):
        return ' '.join([str(i) for i in self.collection])

    def append(self, id):
        priority = self.order_manager.map.get(id).priority
        heappush(self.collection, (priority, id))

        """
        if len(self.collection) > 0:
        
        else:
            
            i = 0
            order = self.order_manager.map.get(id)
            for item in self.collection:
                item_obj = self.order_manager.map.get(item)
                if item_obj.priority >= order.priority:
                    i = i+1
                else:
                    break
            self.collection.insert(i, id) 
            """

    def pop(self):
        priority, item = heappop(self.collection)
        return item

    def peek(self):
        if len(self.collection) == 0:
            raise exceptions.NotAvailableOrder
        return self.collection[0][1]

    def __len__(self):
        return len(self.collection)

