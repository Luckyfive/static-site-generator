import unittest

from blocknode import BlockType
from main import block_to_block_type


class TestBlockNode(unittest.TestCase):
    def test_paragraph(self):
        text = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Test invalid headings
        self.assertEqual(block_to_block_type("####### Invalid Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code(self):
        # Test valid code block
        text = "```\ndef hello():\n    print('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
        # Test invalid code blocks
        self.assertEqual(block_to_block_type("```\nNo closing backticks"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("``\nNot enough backticks\n``"), BlockType.PARAGRAPH)

    def test_quote(self):
        # Test single line quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        # Test multi-line quote
        text = "> This is a quote\n> This is the same quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
        # Test invalid quote (missing > on second line)
        text = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Test single item list
        self.assertEqual(block_to_block_type("- Single item"), BlockType.UNORDERED_LIST)
        # Test multi-item list
        text = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
        # Test invalid list (missing dash on second line)
        text = "- First item\nSecond item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        # Test invalid list (wrong spacing)
        text = "-Wrong spacing"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Test single item list
        self.assertEqual(block_to_block_type("1. Single item"), BlockType.ORDERED_LIST)
        # Test multi-item list
        text = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
        # Test invalid list (wrong order)
        text = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        # Test invalid list (doesn't start at 1)
        text = "2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
        # Test invalid list (wrong spacing)
        text = "1.Wrong spacing"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
