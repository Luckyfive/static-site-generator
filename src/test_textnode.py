import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(repr(node), "TextNode(This is a text node, image, https://example.com/image.png)")

    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(This is a text node, text, None)")


if __name__ == "__main__":
    unittest.main()