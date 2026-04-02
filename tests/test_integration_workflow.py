def test_full_order_workflow(order_factory, repository):
    order = order_factory()

    # Simulate workflow
    order.pay()
    repository.save(order)

    loaded = repository.load(order.order_id)

    loaded.ship()
    repository.save(loaded)

    final = repository.load(order.order_id)

    assert final.state == "Shipped"
    assert any(e["type"] == "PaymentCaptured" for e in final.event_history)
    assert any(e["type"] == "ShipmentCreated" for e in final.event_history)



