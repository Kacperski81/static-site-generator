"""
Utilities for page generation and title extraction.
"""

import re
import os
from pathlib import Path
from src.markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    """
    Extract the h1 header (the line starting with a single #) from markdown.
    
    Args:
        markdown: The markdown string to extract the title from
        
    Returns:
        The title text without the # symbol and whitespace
        
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split("\n")
    
    for line in lines:
        line = line.strip()
        # Check if line starts with exactly one # followed by a space
        if line.startswith("# ") and not line.startswith("## "):
            # Extract the title (everything after "# ")
            title = line[2:].strip()
            return title
    
    # If no h1 header found, raise an exception
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from markdown using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML should be written
        basepath: Base path for site URLs (default: "/")
        
    Prints a message showing the generation process.
    Creates any necessary directories.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    page_content = template_content.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", html_content)

    # Replace href and src attributes with basepath
    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace('src="/', f'src="{basepath}')
    
    # Create directories if they don't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the HTML file
    with open(dest_path, 'w') as f:
        f.write(page_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from markdown files in a directory.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
        basepath: Base path for site URLs (default: "/")
    
    """
    # Convert string paths to Path objects
    content_path = Path(dir_path_content)
    dest_path_obj = Path(dest_dir_path)
    
    for entry in content_path.iterdir():
        if entry.is_file() and entry.suffix == '.md':
            relative_path = entry.relative_to(content_path).with_suffix('.html')
            dest_file = dest_path_obj / relative_path
            generate_page(str(entry), template_path, str(dest_file), basepath)
        elif entry.is_dir():
            next_dest = dest_path_obj / entry.name
            generate_pages_recursive(str(entry), template_path, str(next_dest), basepath)
