import pytest
from src.workflow.order import Order
from src.workflow.event_bus import EventBus
from src.workflow.repository import InMemoryOrderRepository

@pytest.fixture
def event_bus():
    return EventBus()

@pytest.fixture
def order_factory(event_bus):
    def _factory(state="Draft"):
        return Order(
            order_id="1",
            customer_id="c1",
            items=["item1"],
            total_amount=100.0,
            state=state,
            event_bus=event_bus,
        )
    return _factory

@pytest.fixture
def repository():
    return InMemoryOrderRepository()
