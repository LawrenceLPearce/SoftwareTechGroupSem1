from heap_visualiser.heap import Heap


class Event:
    def __init__(self, hour: int, minute: int, priority: int, title: str) -> None:
        self.hour = hour
        self.minute = minute
        self.priority = priority
        self.title = title


class EventQueue:
    def __init__(self) -> None:
        # Heap is a max heap. Make time and priority negative 
        # such that earliest time and low priority 
        # (e.g. priority 1 before priority 2) are first
        self._heap = Heap(key=lambda e: (-e.hour, -e.minute, -e.priority))
    
    def insert(self, event: Event) -> None:
        self._heap.insert(event)
    
    def extract(self) -> Event | None:
        if self._heap.isEmpty():
            return None
        
        return self._heap.remove()
    
    def peek(self) -> Event | None:
        return self._heap.peek()
    
    def get(self, index: int) -> Event | None:
        return self._heap._arr[index]
    
    def leftChild(self, index) -> int:
        return self._heap.leftChild(index)
    
    def rightChild(self, index) -> int:
        return self._heap.rightChild(index)

    def __len__(self) -> int:
        return len(self._heap)