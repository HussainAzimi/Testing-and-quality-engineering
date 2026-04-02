import pytest
from unittest.mock import Mock
from src.workflow.order import InvalidStateTransition


# Valid Transitions
@pytest.mark.parametrize(
    ("starting_state", "action", "expected_state"),
    [
        ("Draft", "pay", "Paid"),
        ("Paid", "ship", "Shipped"),
    ],
)

def test_valid_state_transitions(order_factory, starting_state, action, expected_state):
    order = order_factory(state=starting_state)

    getattr(order, action)()
    assert order.state == expected_state


# Invalid Transitions
@pytest.mark.parametrize(
    ("starting_state", "action"),
    [
        ("Paid", "pay"),
        ("Shipped", "pay"),
        ("Draft", "ship"),
        ("Cancelled", "ship"),
    ],
)
def test_invalid_transitions_raise(order_factory, starting_state, action):
    order = order_factory(state=starting_state)

    with pytest.raises(InvalidStateTransition):
        getattr(order, action)()


# Terminal state behavior
def test_cannot_cancel_shipped_order(order_factory):
    order = order_factory(state="Shipped")

    with pytest.raises(InvalidStateTransition):
        order.cancel()

def test_cancel_from_draft(order_factory):
    order = order_factory(state="Draft")

    order.cancel()

    assert order.state == "Cancelled"


# Event publication
def test_event_published_on_pay(order_factory, event_bus):
    events = []

    def handler(event):
        events.append(event)

    event_bus.subscribe("PaymentCaptured", handler)
    order = order_factory()
    order.pay()

    assert any(e["type"] == "PaymentCaptured" for e in events)


# Interaction tests (mocks)
def test_payment_service_called(order_factory):
    order = order_factory()
    mock_payment = Mock()

    order.pay(payment_service=mock_payment)
    mock_payment.capture.assert_called_once_with(order.total_amount)

def test_shipment_service_called(order_factory):
    order = order_factory(state="Paid")
    mock_shipment = Mock()

    order.ship(shipment_service=mock_shipment)
    mock_shipment.create.assert_called_once_with(order.order_id)
