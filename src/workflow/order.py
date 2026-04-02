from typing import List, Optional

class InvalidStateTransition(Exception):
    pass

class Order:
    def __init__(
            self, 
            order_id: str, 
            customer_id: str, 
            items: List[str], 
            total_amount: float,
            state:str = "Draft", 
            event_bus=None,

          ):
            self.order_id = order_id
            self.customer_id = customer_id
            self.items = items
            self.total_amount = total_amount
            self.state = state
            self.event_bus = event_bus
            self.event_history: List[dict] = []
    
    def _change_state(self, new_state: str):
         old_state = self.state
         self.state = new_state

         event = {
              "type": "OrderStateChanged",
              "order_id": self.order_id,
              "old_state": old_state,
              "new_state": new_state
         }

         self.event_history.append(event)

         if self.event_bus:
              self.event_bus.publish(event)

    def pay(self, payment_service=None):
         if self.state != "Draft":
              raise InvalidStateTransition(f"Cannot pay order in state {self.state}")
         
         if payment_service:
              payment_service.capture(self.total_amount)

         self._change_state("Paid")
         event = {
              "type":"PaymentCaptured",
              "order_id": self.order_id,
              "amount": self.total_amount
         }

         self.event_history.append(event)

         if self.event_bus:
              self.event_bus.publish(event)

    def ship(self, shipment_service=None):
         if self.state != "Paid":
              raise InvalidStateTransition(f"Cannot ship order in state {self.state}")
         
         if shipment_service:
              shipment_service.create(self.order_id)

         self._change_state("Shipped")

         event = {
              "type": "ShipmentCreated",
              "order_id": self.order_id,
              "carrier": "UPS",
         }

         self.event_history.append(event)

         if self.event_bus:
              self.event_bus.publish(event)


    def cancel(self):
         if self.state in ("Shipped", "Cancelled"):
              raise InvalidStateTransition(f"Cannot cancel order in state {self.state}")
         self._change_state("Cancelled")   