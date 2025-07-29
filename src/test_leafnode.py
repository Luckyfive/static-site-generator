import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "testing")
        node2 = LeafNode("p", "testing")
        
        nodeText = node.to_html()
        nodeText2 = node2.to_html()

        self.assertEqual(nodeText, nodeText2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
