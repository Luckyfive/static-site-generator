import unittest
from main import markdown_to_html_node, extract_title
from htmlnode import HTMLNode


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """
> This is a quote
> with multiple lines
> and **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item with **bold**
2. Second item with _italic_
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item with _italic_
- Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_heading(self):
        md = """
# Heading 1
## Heading 2 with _italic_
### Heading 3 with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <i>italic</i></h2><h3>Heading 3 with <code>code</code></h3></div>",
        )


    def test_extract_title(self):
        markdown = "# My Title\n\nSome content"
        self.assertEqual(extract_title(markdown), "My Title")
    
    def test_extract_title_with_multiple_hashes(self):
        markdown = "## Not a title\n# Real Title\n### Another header"
        self.assertEqual(extract_title(markdown), "Real Title")
    
    def test_extract_title_with_extra_spaces(self):
        markdown = "#    Title with spaces    \nContent"
        self.assertEqual(extract_title(markdown), "Title with spaces")
    
    def test_extract_title_no_title(self):
        markdown = "No title here\nJust content\n## Some h2"
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_extract_title_empty_document(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
