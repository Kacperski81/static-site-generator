import sys
import os

# Add parent directory to path so we can import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.textnode import TextNode, TextType
from src.markdown_to_html import markdown_to_html_node
from src.copy_static import copy_dir
from src.page_gen import generate_pages_recursive


def main():
    # Get the root project directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    template_path = os.path.join(project_root, "template.html")
    content_index_path = os.path.join(project_root, "content", "index.md")
    public_index_path = os.path.join(public_dir, "index.html")
    
    print("=" * 60)
    print("Starting Static Site Generator")
    print("=" * 60)
    
    # Copy static files to public directory
    print("\n1. Copying static files...")
    copy_dir(static_dir, public_dir)
    
    print("\n2. Static files copied successfully!")
    
    # Generate the main page
    print("\n3. Generating pages...")
    generate_pages_recursive(os.path.join(project_root, "content"), template_path, public_dir)
    
    print("\n4. Pages generated successfully!")
    print("=" * 60)
    print("Static Site Generator Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()