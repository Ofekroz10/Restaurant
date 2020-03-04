import exceptions
import threading
import back

kitchen_lock = threading.Lock()


class Kitchen:
    TIME_IN_DONE = 60

    def __init__(self, workers, server):
        self.workers = workers
        self.available = workers
        self.order_manager = server.order_m
        self.server = server
        self.in_kitchen = []
        self.done = []

    def make_order(self, order_id):
        if self.available == 0:
            raise exceptions.NotAvailableWorker
        else:
            order = self.order_manager.map.get(order_id)
            with back.Server.wait_lock:
                self.server.order_m.pop_order()
            sec = order.calc_sec()
            # set new timer
            print('sec ', sec)
            print('start work on order ', order_id)
            self.available = self.available - 1
            with kitchen_lock:
                self.in_kitchen.append(order_id)
            timer = threading.Timer(sec, self.after_timer, (order_id,))
            timer.start()

    def after_timer(self, order_id):
        print('order ' + str(order_id) + ' is ready!')
        self.available = self.available + 1
        with kitchen_lock:
            self.in_kitchen.remove(order_id)
            self.done.append(order_id)
        timer = threading.Timer(Kitchen.TIME_IN_DONE, self.remove_done, (order_id,))
        timer.start()
        self.server.prepare_order()

    def remove_done(self, order_id):
        with kitchen_lock:
            self.done.remove(order_id)
