import re
from src.textnode import TextNode, TextType
from nodes_delimiter import split_nodes_delimiter

def extract_markdown_images(text):
    """
    Extracts alt text and image URLs from a markdown-formatted text.

    Args:
        text (str): The markdown text to search for image URLs.
        example: "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)]


    Returns:
        list: A list of tuples, where each tuple contains the alt text and the URL of markdown images
    """
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown links form the text

    Args:
        text (str): The markdown text to search for links.
        example: "This is text with a [link](https://example.com)]  

    Returns:
        list: A list of tuples, where each tuple contains the link text and the URL of markdown links
    """
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes based on markdown image syntax.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        A new list of TextNode objects with text nodes split by images
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images, add the node as-is
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting by each image
        text = old_node.text
        for image_alt, image_url in images:
            # Split by the image markdown
            parts = text.split(f"![{image_alt}]({image_url})", 1)
            
            # Add the text before the image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Continue with the text after the image
            text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text (if not empty)
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes based on markdown link syntax.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        A new list of TextNode objects with text nodes split by links
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links, add the node as-is
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text, splitting by each link
        text = old_node.text
        for link_text, link_url in links:
            # Split by the link markdown
            parts = text.split(f"[{link_text}]({link_url})", 1)
            
            # Add the text before the link (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Continue with the text after the link
            text = parts[1] if len(parts) > 1 else ""
        
        # Add any remaining text (if not empty)
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert a string of text into a list of TextNode objects, splitting by images and links.
    
    Args:
        text: The input string to convert
    
    Returns:
        A list of TextNode objects representing the input text
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    """
    Convert a markdown string into a list of blocks (separated by blank lines).
    
    Args:
        markdown: The input markdown string to convert
    
    Returns:
        A list of strings, where each string is a block of markdown
    """
    # Split by blank lines (one or more newlines)
    raw_blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    blocks = []
    for block in raw_blocks:
        # Strip leading/trailing whitespace from the block
        block = block.strip()
        
        # Strip each line within the block to handle internal indentation
        lines = block.split("\n")
        stripped_lines = [line.strip() for line in lines]
        block = "\n".join(stripped_lines)
        
        # Only add non-empty blocks
        if block:
            blocks.append(block)
    
    return blocks