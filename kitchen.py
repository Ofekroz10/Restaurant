import exceptions
import threading
import back


class Kitchen:

    def __init__(self, workers, server):
        self.workers = workers
        self.available = workers
        self.order_manager = server.order_m
        self.server = server

    def make_order(self, order_id):
        if self.available == 0:
            raise exceptions.NotAvailableWorker
        else:
            order = self.order_manager.map.get(order_id)
            self.server.order_m.pop_order()
            sec = order.calc_sec() / 10
            # set new timer
            print('sec ', sec)
            print('start work on order ', order_id)
            self.available = self.available - 1
            timer = threading.Timer(sec, self.after_timer, (order_id,))
            timer.start()

    def after_timer(self, order_id):
        print('order ' + str(order_id) + ' is ready!')
        self.available = self.available + 1
        self.server.prepare_order()
