from src.htmlnode import ParentNode, LeafNode
from src.textnode import TextNode, TextType
from src.markdown_blocks import block_to_block_type, MarkdownBlockType, markdown_to_blocks
from src.utils import text_to_textnodes


def text_to_children(text):
    """
    Convert inline markdown text to a list of HTMLNode children.
    Parses **bold**, _italic_, `code`, images, and links.
    """
    text_nodes = text_to_textnodes(text)
    children = [TextNode.text_node_to_html_node(node) for node in text_nodes]
    return children


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the # characters to determine heading level
    heading_chars = 0
    for char in block:
        if char == "#":
            heading_chars += 1
        else:
            break
    
    # Extract the heading text (skip the #'s and the space)
    heading_text = block[heading_chars + 1:]
    
    # Parse inline markdown in the heading
    children = text_to_children(heading_text)
    
    # Create the heading node (h1 through h6)
    return ParentNode(f"h{heading_chars}", children)


def code_to_html_node(block):
    """
    Convert a code block to an HTMLNode.
    Code blocks do NOT parse inline markdown.
    """
    # Remove the opening ``` line and closing ``` line
    lines = block.split("\n")
    code_lines = lines[1:-1]  # Skip first and last (the backticks)
    
    # Join lines, preserving internal newlines
    code_text = "\n".join(code_lines)
    
    # Create a code leaf node with the raw text
    code_leaf = LeafNode("code", code_text)
    
    # Wrap in a <pre> tag
    return ParentNode("pre", [code_leaf])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    # Split into lines and remove the > prefix from each
    lines = block.split("\n")
    quote_lines = []
    
    for line in lines:
        # Remove leading "> " or just ">"
        if line.startswith("> "):
            quote_lines.append(line[2:])
        elif line.startswith(">"):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    # Join lines back into one text block
    quote_text = "\n".join(quote_lines)
    
    # Parse inline markdown
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    # Split into lines
    lines = block.split("\n")
    
    # Create <li> nodes for each item
    li_nodes = []
    for line in lines:
        # Remove the "- " prefix
        item_text = line[2:]  # Skip "- "
        
        # Parse inline markdown in each list item
        children = text_to_children(item_text)
        
        # Create the <li> node
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    
    # Wrap all <li> nodes in a <ul>
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    # Split into lines
    lines = block.split("\n")
    
    # Create <li> nodes for each item
    li_nodes = []
    for line in lines:
        # Remove the "N. " prefix (e.g., "1. ", "2. ")
        # Find the position of the first dot and space
        dot_index = line.find(". ")
        item_text = line[dot_index + 2:]  # Skip "N. "
        
        # Parse inline markdown in each list item
        children = text_to_children(item_text)
        
        # Create the <li> node
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    
    # Wrap all <li> nodes in an <ol>
    return ParentNode("ol", li_nodes)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Join lines with a space (paragraphs can span multiple lines)
    paragraph_text = " ".join(block.split("\n"))
    
    # Parse inline markdown
    children = text_to_children(paragraph_text)
    
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode (div).
    The div contains one child node per markdown block.
    """
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Convert each block to an HTMLNode
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == MarkdownBlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == MarkdownBlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == MarkdownBlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == MarkdownBlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == MarkdownBlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:  # PARAGRAPH
            node = paragraph_to_html_node(block)
        
        block_nodes.append(node)
    
    # Return everything wrapped in a div
    return ParentNode("div", block_nodes)