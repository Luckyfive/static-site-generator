import unittest

from htmlnode import HTMLNode
from main import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "testing")
        node2 = HTMLNode("p", "testing")
        
        nodeText = node.props_to_html()
        nodeText2 = node2.props_to_html()

        self.assertEqual(nodeText, nodeText2)

if __name__ == "__main__":
    unittest.main()