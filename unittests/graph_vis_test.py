import unittest
from graph_traversal.graph import Graph


def build_tutorial_graph() -> Graph:
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'F')
    return g


class TestBFS(unittest.TestCase):

    def test_bfs_visits_all_nodes(self):
        # this runs BFS from 'A' node, and checks all the nodes
        g = build_tutorial_graph()
        result = g.bfs('A')
        self.assertEqual(sorted(result), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_bfs_start_node_is_first(self):
        # this checks that the node you start from is always first in the output/end result
        g = build_tutorial_graph()
        self.assertEqual(g.bfs('A')[0], 'A')
        self.assertEqual(g.bfs('C')[0], 'C')

    def test_bfs_order_from_a(self):
        # this checks that the BFS is doing what its supposed to (like B has to appear before D)
        g = build_tutorial_graph()
        result = g.bfs('A')
        self.assertLess(result.index('B'), result.index('D'))
        self.assertLess(result.index('B'), result.index('E'))
        self.assertLess(result.index('C'), result.index('F'))

    def test_bfs_no_duplicates(self):
        # this checks that no node appears twice
        g = build_tutorial_graph()
        result = g.bfs('A')
        self.assertEqual(len(result), len(set(result)))

    def test_bfs_single_node(self):
        # makes a graph with just one node return that node exclusively
        g = Graph()
        g.add_node('X')
        self.assertEqual(g.bfs('X'), ['X'])


class TestDFS(unittest.TestCase):

    def test_dfs_visits_all_nodes(self):
        # same as BFS variant, just for depth-first
        g = build_tutorial_graph()
        result = g.dfs('A')
        self.assertEqual(sorted(result), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_dfs_start_node_is_first(self):
        # same as BFS variant, just for depth-first
        g = build_tutorial_graph()
        self.assertEqual(g.dfs('A')[0], 'A')
        self.assertEqual(g.dfs('D')[0], 'D')

    def test_dfs_goes_deep_before_wide(self):
        # checks that D appears before C to show that DFS goes through the B branch and goes back to C
        g = build_tutorial_graph()
        result = g.dfs('A')
        self.assertLess(result.index('D'), result.index('C'))

    def test_dfs_no_duplicates(self):
        # same as BFS variant, just for depth-first
        g = build_tutorial_graph()
        result = g.dfs('A')
        self.assertEqual(len(result), len(set(result)))

    def test_dfs_single_node(self):
        # same as BFS variant, just for depth-first
        g = Graph()
        g.add_node('X')
        self.assertEqual(g.dfs('X'), ['X'])


class TestBFSvsDFS(unittest.TestCase):

    def test_bfs_and_dfs_visit_same_nodes(self):
        # makes DFS and BFS visit all the same nodes, just in their different order.
        g = build_tutorial_graph()
        self.assertEqual(set(g.bfs('A')), set(g.dfs('A')))

    def test_bfs_and_dfs_produce_different_order(self):
        # verifies that the two algorithms have different results and reinforcing that they do different things.
        g = build_tutorial_graph()
        self.assertNotEqual(g.bfs('A'), g.dfs('A'))


if __name__ == "__main__":
    unittest.main(verbosity=2)