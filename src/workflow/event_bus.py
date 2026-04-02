from typing import Callable, Dict, List, Tuple

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Tuple[int, int, Callable]]] = {}
        self._counter = 0
        self.dead_letters: List[Tuple] = []

    
    def subscribe(self, event_type: str, handler: Callable, priority: int= 0):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._counter += 1
        self._subscribers[event_type].append((priority, self._counter, handler))

    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            return
        new_handlers = []

        for priority, counter, h in self._subscribers[event_type]:
            if h is not handler:
                new_handlers.append((priority, counter, h))
        
        self._subscribers[event_type] =  new_handlers
               
    
    def publish(self, event: dict):
        event_type = event.get("type", "")

        handlers = self._subscribers.get(event_type, [])

        handlers = sorted(handlers, key=lambda x: (-x[0], x[1]))

        for _, _, handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self.dead_letters.append((event, handler, str(e)))