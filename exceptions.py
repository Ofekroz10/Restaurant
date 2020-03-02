class NotAvailableWorker(Exception):
    """ represent state that there is no available worker for prepare the meal """
    pass


class NotAvailableOrder(Exception):
    """ represent state that there is no available order in the queue """
    pass
