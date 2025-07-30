from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
        dummyNode = TextNode("This is some anchor text", TextType.LINK, "https://example.com")
        print(dummyNode)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    raise Exception("Invalid TextNode TextType encountered.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, part in enumerate(sections):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, old_node.text_type))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

if __name__ == "__main__":
    main()