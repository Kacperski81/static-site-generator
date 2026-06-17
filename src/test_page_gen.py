import unittest
from page_gen import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        """Test extracting a simple h1 title"""
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")
    
    def test_extract_title_with_content(self):
        """Test extracting title with other content"""
        md = """# My Title

This is some content below the title.
"""
        self.assertEqual(extract_title(md), "My Title")
    
    def test_extract_title_with_whitespace(self):
        """Test that whitespace is stripped"""
        md = "#   Whitespace Title   "
        self.assertEqual(extract_title(md), "Whitespace Title")
    
    def test_extract_title_with_multiple_words(self):
        """Test title with multiple words"""
        md = "# Tolkien Fan Club"
        self.assertEqual(extract_title(md), "Tolkien Fan Club")
    
    def test_extract_title_ignores_h2(self):
        """Test that h2 headers are ignored"""
        md = """## Not the title

# This is the title
"""
        self.assertEqual(extract_title(md), "This is the title")
    
    def test_extract_title_no_h1_raises(self):
        """Test that ValueError is raised when no h1 is found"""
        md = """## Just h2

### And h3

Some content
"""
        with self.assertRaises(ValueError) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_extract_title_only_hash_raises(self):
        """Test that a lone # without content is handled"""
        md = "#"
        with self.assertRaises(ValueError):
            extract_title(md)
    
    def test_extract_title_with_special_chars(self):
        """Test title with special characters"""
        md = "# Why Glorfindel is > Legolas!"
        self.assertEqual(extract_title(md), "Why Glorfindel is > Legolas!")


if __name__ == "__main__":
    unittest.main()
