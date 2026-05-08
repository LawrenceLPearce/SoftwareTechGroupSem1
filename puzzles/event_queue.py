from heap_visualiser.heap import Heap


class Event:
    def __init__(self, time: int, priority: int, description: str) -> None:
        self.time = time
        self.priority = priority
        self.description = description


class EventQueue:
    def __init__(self) -> None:
        self._heap = Heap(key=lambda e: (-e.time, e.priority))
    
    def insert(self, event: Event) -> None:
        self._heap.insert(event)
    
    def extract(self) -> Event | None:
        if self._heap.isEmpty():
            return None
        
        return self._heap.remove()
    
    def peek(self) -> Event | None:
        return self._heap.peek()