"""This file contains tests for the sorting algorithms. Note that since no headless mode is implemented, pygame must be
launched."""
import unittest
import pygame
from sort_algorithms.sorting_algorithms import bubble_sort_visualiser, selection_sort_visualiser, merge_sort_iterative


class TestBubbleSort(unittest.TestCase):

    def setUp(self):
        self.screen = pygame.display.set_mode((900, 600))

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        bubble_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_random(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        bubble_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, sorted(arr))

    def test_single_element(self):
        arr = [42]
        bubble_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [42])

    def test_duplicates(self):
        arr = [3, 1, 2, 3, 1]
        bubble_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [1, 1, 2, 3, 3])


class TestSelectionSort(unittest.TestCase):

    def setUp(self):
        self.screen = pygame.display.set_mode((900, 600))

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        selection_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_random(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        selection_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, sorted(arr))

    def test_single_element(self):
        arr = [42]
        selection_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [42])

    def test_duplicates(self):
        arr = [3, 1, 2, 3, 1]
        selection_sort_visualiser(arr, self.screen, 0)
        self.assertEqual(arr, [1, 1, 2, 3, 3])


class TestMergeSort(unittest.TestCase):

    def setUp(self):
        self.screen = pygame.display.set_mode((900, 600))

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        merge_sort_iterative(arr, self.screen, 0)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_random(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = sorted(arr)
        merge_sort_iterative(arr, self.screen, 0)
        self.assertEqual(arr, expected)

    def test_single_element(self):
        arr = [42]
        merge_sort_iterative(arr, self.screen, 0)
        self.assertEqual(arr, [42])

    def test_duplicates(self):
        arr = [3, 1, 2, 3, 1]
        merge_sort_iterative(arr, self.screen, 0)
        self.assertEqual(arr, [1, 1, 2, 3, 3])


def main():
    pygame.init()
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()

