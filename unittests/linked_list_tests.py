import unittest
from DSP.linked_list import LinkedList


def make_linked_list() -> LinkedList:
    linked_list = LinkedList()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        linked_list.insert(val, 0)
    return linked_list
        

class TestInsert(unittest.TestCase):
    def test_insert(self):
        linked_list = make_linked_list()
        linked_list.insert(100, 2)
        self.assertEqual(linked_list.head.next.next.data, 100)


class TestDelete(unittest.TestCase):
    def test_delete(self):
        linked_list = make_linked_list()
        linked_list.delete(80) # Delete head
        self.assertEqual(linked_list.head.data, 60)


class TestReverse(unittest.TestCase):
    def test_reverse(self):
        linked_list = LinkedList()
        linked_list.insert(1, 0)
        linked_list.insert(2, 1)
        linked_list.insert(3, 2)
        linked_list.insert(4, 3)

        linked_list.reverse()

        # Iterate through list and track order
        visited = []
        current = linked_list.head
        while current:
            visited.append(current.data)
            current = current.next

        self.assertEqual(visited, [4, 3, 2, 1])


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()