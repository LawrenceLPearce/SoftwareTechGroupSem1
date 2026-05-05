import unittest
from heap_visualiser.heap import Heap


def make_heap() -> Heap:
    default_values = [1, 3, 4, 10, 20, 35, 5]
    heap = Heap(size=len(default_values))

    for value in default_values:
        heap.insert(value)
    
    return heap


class TestInsert(unittest.TestCase):
    def test_insert(self):
        heap = make_heap()
        heap.insert(100)
        self.assertEqual(heap.peek(), 100)


class TestExtract(unittest.TestCase):
    def test_extract(self):
        heap = make_heap()
        heap.remove()
        self.assertEqual(heap.peek(), 20)


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()