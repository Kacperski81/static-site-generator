import unittest
from markdown_blocks import MarkdownBlockType, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_block_to_block_heading_one(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.HEADING)

    def test_block_to_block_heading_six(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.HEADING)
    
    def test_block_to_block_heading_invalid(self):
        block = "####### Heading"
        self.assertNotEqual(block_to_block_type(block), MarkdownBlockType.HEADING)

    def test_block_to_block_code(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.CODE)
    
    def test_block_to_block_quote(self):
        block = "> Quote"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.QUOTE)
    
    def test_block_to_block_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.UNORDERED_LIST)

    def test_block_to_block_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.ORDERED_LIST)