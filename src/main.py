from textnode import TextNode, TextType
from leafnode import LeafNode
from blocknode import BlockType
import re

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

def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        matches = extract_markdown_images(current_text)
        
        if not matches:
            new_nodes.append(old_node)
            continue
            
        remaining_text = current_text
        for match in matches:
            image_text, image_url = match
            parts = remaining_text.split(f"![{image_text}]({image_url})", 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        matches = extract_markdown_links(current_text)
        
        if not matches:
            new_nodes.append(old_node)
            continue
            
        remaining_text = current_text
        for match in matches:
            link_text, link_url = match
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

def markdown_to_blocks(markdown):
    result = []
    new_blocks = markdown.split("\n\n")
    for i, block in enumerate(new_blocks):
        curr_block = block.strip()
        if not curr_block:
            continue
        result.append(block.strip())
    return result

def block_to_block_type(block):
    # Check for headings (1-6 # characters)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code blocks (must start AND end with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check quote block (every line must start with >)
    lines = block.split('\n')
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    
    # Check unordered list (every line must start with -)
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check ordered list (must start at 1 and increment)
    if all(bool(re.match(r'^\d+\. ', line)) for line in lines):
        # Extract the numbers and check if they form a sequence starting at 1
        numbers = [int(re.match(r'^(\d+)\.', line).group(1)) for line in lines]
        if numbers[0] == 1 and all(numbers[i] == numbers[i-1] + 1 for i in range(1, len(numbers))):
            return BlockType.ORDERED_LIST
    
    # Default to paragraph if no other type matches
    return BlockType.PARAGRAPH

if __name__ == "__main__":
    main()