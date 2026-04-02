def test_subscribe_and_publish(event_bus):
    calls = []

    def handler(event):
        calls.append(event)

    event_bus.subscribe("test_event", handler)
    event_bus.publish({"type": "test_event"})

    assert len(calls) == 1


def test_unsubscribe(event_bus):
    calls = []

    def handler(event):
        calls.append(event)

    event_bus.subscribe("test_event", handler)
    event_bus.unsubscribe("test_event", handler)

    event_bus.publish({"type": "test_event"})
    
    assert len(calls) == 0

def test_priority_ordering(event_bus):
    calls = []

    def low(event):
        calls.append("low")

    def high(event):
        calls.append("high")


    event_bus.subscribe("test", low, priority=1)
    event_bus.subscribe("test", high, priority=10)

    event_bus.publish({"type": "test"})

    assert calls == ["high", "low"]

def test_fifo_when_same_priority(event_bus):
    calls = []

    def first(event):
        calls.append("first")

    def second(event):
        calls.append("second")

    event_bus.subscribe("test", first, priority=5)
    event_bus.subscribe("test", second, priority=5)

    event_bus.publish({"type": "test"})

    assert calls == ["first", "second"]

def test_dead_letter_on_handler_failure(event_bus):
    def bad_handler(event):
        raise Exception("fail")
    
    event_bus.subscribe("test", bad_handler)
    event_bus.publish({"type": "test"})

    assert len(event_bus.dead_letters) == 1
