import unittest
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DSP.stack import Stack
from DSP.queue_script import Queue

class TestStack(unittest.TestCase):
    def test_push_increases_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.size(), 2)

    def test_pop_returns_lifo_order(self):
        # this test pushes three units and then pops
        s = Stack()
        for v in [10, 20, 30]:
            s.push(v)
        self.assertEqual(s.pop(), 30)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)

    def test_pop_decreases_size(self):
        s = Stack()
        s.push(5)
        s.push(6)
        s.pop()
        self.assertEqual(s.size(), 1)

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(99)
        self.assertEqual(s.peek(), 99)
        self.assertEqual(s.size(), 1)   # still there

    def test_is_empty_on_new_stack(self):
        self.assertTrue(Stack().is_empty())

    def test_is_empty_after_all_pops(self):
        s = Stack()
        s.push(1)
        s.pop()
        self.assertTrue(s.is_empty())

    def test_not_empty_after_push(self):
        s = Stack()
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_push3_pop2_final_size(self):
        # test case for pushing 3 units then popping 2
        s = Stack()
        s.push("A")
        s.push("B")
        s.push("C")
        s.pop()
        s.pop()
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.peek(), "A")

    # error cases
    def test_pop_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            Stack().pop()

    def test_peek_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            Stack().peek()

    def test_large_push_pop_sequence(self):
        # stress-test that pushes 1000 items and pops all of them, checking that LIFO order is maintained
        s = Stack()
        n = 1_000
        for i in range(n):
            s.push(i)
        self.assertEqual(s.size(), n)
        for i in reversed(range(n)):
            self.assertEqual(s.pop(), i)
        self.assertTrue(s.is_empty())

    def test_benchmark_push_pop(self):
        # tests push/pop with a value of 1,000,000
        s = Stack()
        n = 1_000_000
        start = time.perf_counter()
        for i in range(n):
            s.push(i)
        for _ in range(n):
            s.pop()
        elapsed = time.perf_counter() - start
        print(f"\nStack benchmark - unit count {n:,} pushed and popped in {elapsed:.4f}s")
        self.assertLess(elapsed, 5.0,
                        "Stack benchmark took longer than 5 seconds")

class TestQueue(unittest.TestCase):
    def test_enqueue_increases_size(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.size(), 2)

    def test_dequeue_returns_fifo_order(self):
        # test case for enqueueing 3 units then deque 2
        q = Queue()
        for v in [10, 20, 30]:
            q.enqueue(v)
        self.assertEqual(q.dequeue(), 10)
        self.assertEqual(q.dequeue(), 20)
        self.assertEqual(q.dequeue(), 30)

    def test_dequeue_decreases_size(self):
        q = Queue()
        q.enqueue(5)
        q.enqueue(6)
        q.dequeue()
        self.assertEqual(q.size(), 1)

    def test_peek_returns_front_without_removing(self):
        q = Queue()
        q.enqueue(7)
        q.enqueue(8)
        self.assertEqual(q.peek(), 7)
        self.assertEqual(q.size(), 2)   # still 2 items

    def test_is_empty_on_new_queue(self):
        self.assertTrue(Queue().is_empty())

    def test_is_empty_after_all_dequeues(self):
        q = Queue()
        q.enqueue(1)
        q.dequeue()
        self.assertTrue(q.is_empty())

    def test_not_empty_after_enqueue(self):
        q = Queue()
        q.enqueue(1)
        self.assertFalse(q.is_empty())

    def test_enqueue4_dequeue3_fifo(self):
        # enqueue 4 units and then dequeue 3 and making sure order is First In First Out.
        q = Queue()
        for v in [1, 2, 3, 4]:
            q.enqueue(v)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.size(), 1)
        self.assertEqual(q.peek(), 4)

    def test_dequeue_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            Queue().dequeue()

    def test_peek_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            Queue().peek()

    def test_large_enqueue_dequeue_sequence(self):
        # this test enqueues 1000 units, then all of them are dequeued, making sure it is First In First Out
        q = Queue()
        n = 1_000
        for i in range(n):
            q.enqueue(i)
        self.assertEqual(q.size(), n)
        for i in range(n):
            self.assertEqual(q.dequeue(), i)
        self.assertTrue(q.is_empty())

    def test_benchmark_enqueue_dequeue(self):
        # tests push/pop with a value of 1,000,000
        q = Queue()
        n = 1_000_000
        start = time.perf_counter()
        for i in range(n):
            q.enqueue(i)
        for _ in range(n):
            q.dequeue()
        elapsed = time.perf_counter() - start
        print(f"\nQueue benchmark - unit count {n:,} enqueued and dequeued in {elapsed:.4f}s")
        self.assertLess(elapsed, 5.0,
                        "Queue benchmark took longer than 5 seconds")


if __name__ == "__main__":
    unittest.main(verbosity=2)