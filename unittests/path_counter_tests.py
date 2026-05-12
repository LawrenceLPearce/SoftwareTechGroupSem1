import unittest

from puzzles.node_graph import Graph

def make_graph(rows, cols):
    return Graph(rows, cols, cell_size=10, screen=None, background_rect=None, headless=True)

class PathCounterTest(unittest.TestCase):


    def make_graph(self, rows, cols):
        self.graph = make_graph(rows, cols)
        self.graph.set_start_node(self.graph.get_node(0, 0))
        self.graph.set_end_node(self.graph.get_node(-1, -1))


    def test_multiple_counts(self):
        known_counts = {
            2: 2,
            3: 12,
            4: 184,
            5: 8512,
            6: 1_262_816,
        }

        for size, answer in known_counts.items():
            with self.subTest(size=size):
                self.make_graph(size, size)
                count = self.graph.run_route_count()[0]
                self.assertEqual(count, answer)

    def test_valid_path(self):
        self.make_graph(3, 3)

        path = self.graph.run_route_count()[1]
        self.assertIsNotNone(path)
        self.assertIsNot(path, [])

    def test_paths_are_random(self):
        self.make_graph(3, 3)

        path_a = self.graph.run_route_count()[1]
        path_b = self.graph.run_route_count()[1]

        self.assertNotEqual(path_a, path_b)