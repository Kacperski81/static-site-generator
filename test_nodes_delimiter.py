import unittest
from src.textnode import TextNode, TextType
from nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    # Basic functionality tests
    def test_split_code_delimiter(self):
        """Test splitting with backtick delimiter for code"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_bold_delimiter(self):
        """Test splitting with double asterisk delimiter for bold"""
        node = TextNode("This is **bold text** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_italic_delimiter(self):
        """Test splitting with underscore delimiter for italic"""
        node = TextNode("This is _italic text_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # Multiple delimiters in one text
    def test_multiple_delimiters(self):
        """Test text with multiple delimiter pairs"""
        node = TextNode("This has `code1` and `code2` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # Non-text nodes should be passed through unchanged
    def test_non_text_nodes_unchanged(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(new_nodes, nodes)
    
    def test_mixed_text_and_non_text_nodes(self):
        """Test a mix of TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("This is `code` text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("More `code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # Edge cases
    def test_empty_node_list(self):
        """Test with empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])
    
    def test_delimiter_at_start(self):
        """Test delimiter at the start of text"""
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        node = TextNode("at end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_only_delimited_text(self):
        """Test text that is entirely within delimiters"""
        node = TextNode("`entire code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("entire code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_text_with_url(self):
        """Test that node with URL is preserved through splitting"""
        node = TextNode("Link with `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Link with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # Multi-character delimiters
    def test_multi_char_delimiter(self):
        """Test with multi-character delimiters like **"""
        node = TextNode("Start **bold** middle **more bold** end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # Error cases
    def test_unmatched_delimiter_error(self):
        """Test that unmatched delimiters raise ValueError"""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("Unmatched delimiter", str(context.exception))
        self.assertIn("`", str(context.exception))
    
    def test_three_delimiters_error(self):
        """Test that odd number of delimiters raises error"""
        node = TextNode("`code1` and `code2` and `code3", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    # Chaining multiple delimiter operations
    def test_chaining_operations(self):
        """Test chaining multiple split operations for different delimiters"""
        # Start with text containing both bold and code
        node = TextNode("Text with **bold** and `code`", TextType.TEXT)
        
        # First split on bold markers
        after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Then split the TEXT nodes on code markers
        final_nodes = split_nodes_delimiter(after_bold, "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(final_nodes, expected)
    
    # Special characters
    def test_special_char_delimiter(self):
        """Test with special character delimiters"""
        node = TextNode("Text with |special| content", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "|", TextType.BOLD)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("special", TextType.BOLD),
            TextNode(" content", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_consecutive_delimiters(self):
        """Test with consecutive delimiters (empty content)"""
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Empty strings are skipped, so only non-empty parts are added
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_single_delimiter_pair(self):
        """Test a simple single delimiter pair"""
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_three_pairs_of_delimiters(self):
        """Test with three pairs of delimiters"""
        node = TextNode("`a` and `b` and `c`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("a", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("c", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == '__main__':
    unittest.main()
