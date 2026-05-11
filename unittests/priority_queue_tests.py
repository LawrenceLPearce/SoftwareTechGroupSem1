import unittest
from puzzles.event_queue import Event, EventQueue


def make_queue() -> EventQueue:
    """Makes a priority queue with 5 events."""
    queue = EventQueue()

    events = [
        Event(12, 30, 1, "Event 1"), Event(9, 15, 2, "Event 2"),
        Event(12, 30, 2, "Event 3"), Event(13, 45, 1, "Event 4"),
        Event(6, 0, 1, "Event 5")
    ]

    for event in events:
        queue.insert(event)
    
    return queue


class TestInsert(unittest.TestCase):
    def test_insert(self):
        queue = make_queue()

        # Ensure event of earliest time is at root
        new_event = Event(1, 30, 2, "New event")
        queue.insert(new_event)
        self.assertEqual(queue.get(0), new_event)
        
        # Ensure event of same time with 'higher' priority is at root
        new_event = Event(1, 30, 1, "New event 2")
        queue.insert(new_event)
        self.assertEqual(queue.get(0), new_event)


class TestInsert2(unittest.TestCase):
    def test_insert(self):
        queue = make_queue()

        # Ensure event of same time with 'higher' priority is at root
        new_event = Event(1, 30, 2, "New event")
        queue.insert(new_event)
        new_event = Event(1, 30, 1, "New event 2")
        queue.insert(new_event)
        self.assertEqual(queue.get(0), new_event)


class TestExtract(unittest.TestCase):
    def test_insert(self):
        queue = make_queue()

        # Ensure event of earliest time is at root
        queue.remove()
        self.assertEqual(
            (queue.get(0).hour, queue.get(0).minute, # type: ignore
            queue.get(0).priority, queue.get(0).title), # type: ignore
            (9, 15, 2, "Event 2")
        )


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()