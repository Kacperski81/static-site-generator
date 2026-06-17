from src.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Split text nodes based on a delimiter and text type.
    
    Args:
        old_nodes: List of TextNode objects to process
        delimiter: The delimiter string to split on (e.g., "`" for code, "**" for bold, "_" for italic)
        text_type: The TextType to apply to delimited sections
        
    Returns:
        A new list of TextNode objects with text nodes split according to the delimiter
        
    Raises:
        ValueError: If a closing delimiter is not found (unmatched delimiters)
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # Check if we have unmatched delimiters (even number of parts means unmatched)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {old_node.text}")
        
        # Process the parts, alternating between TEXT and the specified text_type
        for i, part in enumerate(parts):
            if part:  # Skip empty strings
                if i % 2 == 0:
                    # Even index = TEXT type
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    # Odd index = the specified text_type
                    new_nodes.append(TextNode(part, text_type))
    
    return new_nodes