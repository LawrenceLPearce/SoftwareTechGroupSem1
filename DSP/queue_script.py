"""Minimal queue implementation. Python file is named queue_script.py to avoid overriding built in python library"""

from collections import deque


class Queue:
    def __init__(self):
        self._data = deque()

    # inserts a value that goes into the back of queue
    def enqueue(self, val):
        self._data.append(val)

    # removes the front value and also returns what was removed
    def dequeue(self):
        if not self.is_empty():
            return self._data.popleft()
        raise IndexError("dequeue from empty queue")

    def peek(self):
        if not self.is_empty():
            return self._data[0]
        raise IndexError("peek from empty queue")

    def is_empty(self):
        return len(self._data) == 0

    # shows size of list
    def size(self):
        return len(self._data)

    def items(self):
        return list(self._data)

    def __repr__(self):
        return f"Queue({list(self._data)})"
