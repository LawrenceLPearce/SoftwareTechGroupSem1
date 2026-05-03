import unittest
from DSP.binary_search_tree import BST


class TestInsert(unittest.TestCase):

    def test_insert_structure(self):
        bst = BST()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(val)
        self.assertEqual(bst.root.val, 50)
        self.assertEqual(bst.root.left.val, 30)
        self.assertEqual(bst.root.right.val, 70)


class TestInorder(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(val)

    def test_inorder_is_sorted(self):
        id_to_val = {}
        def collect(node):
            if node:
                id_to_val[id(node)] = node.val
                collect(node.left)
                collect(node.right)
        collect(self.bst.root)
        values = [id_to_val[nid] for nid in self.bst.inorder()]
        self.assertEqual(values, sorted(values))


class TestPreorder(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(val)

    def test_preorder_root_first(self):
        self.assertEqual(self.bst.preorder()[0], id(self.bst.root))


class TestPostorder(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(val)

    def test_postorder_root_last(self):
        self.assertEqual(self.bst.postorder()[-1], id(self.bst.root))


class TestTraversalsCombined(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
        for val in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(val)

    def test_all_same_nodes(self):
        self.assertEqual(set(self.bst.inorder()), set(self.bst.preorder()))
        self.assertEqual(set(self.bst.preorder()), set(self.bst.postorder()))

    def test_traversals_differ(self):
        self.assertNotEqual(self.bst.inorder(),  self.bst.preorder())
        self.assertNotEqual(self.bst.inorder(),  self.bst.postorder())
        self.assertNotEqual(self.bst.preorder(), self.bst.postorder())


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()