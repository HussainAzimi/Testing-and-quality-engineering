class InMemoryOrderRepository:
    def __init__(self):
        self.storage = {}

    def save(self, order):
        self.storage[order.order_id] = order

    def load(self, order_id):
        return self.storage.get(order_id)