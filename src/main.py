from textnode import TextNode, TextType
from leafnode import LeafNode
from blocknode import BlockType
from htmlnode import HTMLNode
import re

def copy_files_recursive(src_dir, dest_dir):
    """
    Recursively copy files from src_dir to dest_dir.
    First cleans the destination directory if it exists.
    """
    import os
    import shutil

    # If destination exists, remove it
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.makedirs(dest_dir)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        # Calculate the corresponding destination directory
        rel_path = os.path.relpath(root, src_dir)
        dest_root = os.path.join(dest_dir, rel_path)
        
        # Create all subdirectories
        for dir_name in dirs:
            dest_path = os.path.join(dest_root, dir_name)
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path, exist_ok=True)
        
        # Copy all files
        for file_name in files:
            src_path = os.path.join(root, file_name)
            dest_path = os.path.join(dest_root, file_name)
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy2(src_path, dest_path)

def main():
    # Define source and destination directories relative to the project root
    import os
    
    # Get the project root directory (parent of src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(project_root, "static")
    dest_dir = os.path.join(project_root, "public")
    
    # Copy static files to public directory
    copy_files_recursive(src_dir, dest_dir)
    
    print("Static files copied successfully!")

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
    # Split on empty lines (one or more newlines)
    blocks = [b.strip() for b in re.split(r'\n\s*\n', markdown)]
    for block in blocks:
        if not block:  # Skip empty blocks
            continue
        # Split blocks further if they contain headings
        if '\n#' in block:
            # Split on newlines followed by #
            sub_blocks = re.split(r'\n(?=#)', block)
            result.extend(b.strip() for b in sub_blocks if b.strip())
        else:
            result.append(block)
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

def markdown_to_html_node(markdown):
    """Convert a markdown document to an HTML node"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        # Clean up newlines in the block itself
        block = ' '.join([line.strip() for line in block.split('\n')])
        child = block_to_html_node(block)
        children.append(child)
    return HTMLNode("div", None, children)

def text_to_children(text):
    """Convert a text string to a list of inline HTML nodes"""
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def get_heading_level(block):
    """Get the heading level (1-6) from a heading block"""
    match = re.match(r'^(#{1,6})\s', block)
    if match:
        return len(match.group(1))
    return 0

def block_to_html_node(block):
    """Convert a block of text to its corresponding HTML node"""
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        # Convert newlines to spaces in paragraphs
        text = ' '.join(line.strip() for line in block.split('\n'))
        return HTMLNode("p", None, text_to_children(text))
        
    if block_type == BlockType.HEADING:
        level = get_heading_level(block)
        text = block.lstrip('#').strip()  # Remove the #s and whitespace
        return HTMLNode(f"h{level}", None, text_to_children(text))
        
    if block_type == BlockType.CODE:
        # Remove the first and last ``` and preserve internal newlines
        lines = block.split('\n')
        if len(lines) >= 2:  # If there are at least 2 lines
            code = '\n'.join(lines[1:-1])  # Skip first and last line containing ```
        else:
            code = block.strip('`').strip()
        # Ensure the code block ends with a newline
        if not code.endswith('\n'):
            code += '\n'
        # Create a text node that won't process markdown
        text_node = TextNode(code, TextType.TEXT)
        code_node = text_node_to_html_node(text_node)
        return HTMLNode("pre", None, [HTMLNode("code", None, [code_node])])
        
    if block_type == BlockType.QUOTE:
        # Remove > from each line and join with spaces
        text = ' '.join(line.lstrip('> ').strip() for line in block.split('\n'))
        return HTMLNode("blockquote", None, text_to_children(text))
        
    if block_type == BlockType.UNORDERED_LIST:
        items = []
        for line in block.split('\n'):
            text = line.lstrip('- ').strip()
            items.append(HTMLNode("li", None, text_to_children(text)))
        return HTMLNode("ul", None, items)
        
    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in block.split('\n'):
            text = re.sub(r'^\d+\.\s+', '', line).strip()
            items.append(HTMLNode("li", None, text_to_children(text)))
        return HTMLNode("ol", None, items)
    
    raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown):
    """Convert a markdown document to an HTML node"""
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        child = block_to_html_node(block)
        children.append(child)
    return HTMLNode("div", None, children)

if __name__ == "__main__":
    main()