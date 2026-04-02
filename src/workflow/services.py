from typing import Any


class FakePaymentService:
    def __init__(self):
        self.calls = []

    def capture(self, amount):
        self.calls.append(amount)

class FakeShipmentService:
    def __init__(self):
        self.calls = []

    def create(self, order_id):
        self.calls.append(order_id)