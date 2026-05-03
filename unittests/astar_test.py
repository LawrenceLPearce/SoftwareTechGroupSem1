import unittest
from path_finder_puzzle.node_graph import Graph


def make_graph(rows, cols):
    return Graph(rows, cols, cell_size=10, screen=None, background_rect=None, headless=True)


class TestAStarSearch(unittest.TestCase):

    def setUp(self):
        self.graph = make_graph(5, 5)
        self.graph.set_start_node(self.graph.get_node(0, 0))
        self.graph.set_end_node(self.graph.get_node(4, 4))

    def test_simple_path_found(self):
        path = self.graph.a_star_search()
        self.assertIsNotNone(path)

    def test_path_starts_and_ends(self):
        path = self.graph.a_star_search()
        self.assertEqual(path[0], self.graph.start_node)
        self.assertEqual(path[-1], self.graph.end_node)

    def test_path_blocked_returns_none(self):
        self.graph.set_start_node(self.graph.get_node(0, 0))
        self.graph.set_end_node(self.graph.get_node(0, 2))
        self.graph.get_node(0, 1).set_obstacle_true()
        self.graph.get_node(1, 2).set_obstacle_true()
        self.graph.get_node(0, 3).set_obstacle_true()
        path = self.graph.a_star_search()
        self.assertIsNone(path)

    def test_path_nodes_are_neighbours(self):
        path = self.graph.a_star_search()
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], path[i].neighbours)


class TestPriorityQueue(unittest.TestCase):

    def test_priority_queue_order(self):
        graph = make_graph(3, 3)
        nodes = [graph.get_node(0, c) for c in range(3)]
        f_values = [7, 2, 5]
        queue = []
        for node, f in zip(nodes, f_values):
            node.f = f
            Graph.priority_f_queue_insert(queue, node)
        self.assertEqual([n.f for n in queue], [2, 5, 7])


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()