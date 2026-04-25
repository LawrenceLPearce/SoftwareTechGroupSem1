# the code used here was from the Week 10 tutorial sheet (Task 1.3)
class Stack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if not self.is_empty():
            return self._data.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self._data[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def items(self):
        return list(self._data)

    def __repr__(self):
        return f"Stack({self._data})"
