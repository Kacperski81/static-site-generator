import unittest
from src.utils import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from src.textnode import TextNode, TextType

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple_images(self):
        text = "This is text with ![image1](https://example.com/image1.png) and ![image2](https://example.com/image2.png)"
        expected = [("image1", "https://example.com/image1.png"), ("image2", "https://example.com/image2.png")]
        self.assertEqual(extract_markdown_images(text), expected)
    
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)")
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_markdown_links_multiple_links(self):
        text = "This is text with [link1](https://example.com/link1) and [link2](https://example.com/link2)"
        expected = [("link1", "https://example.com/link1"), ("link2", "https://example.com/link2")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_image_no_images(self):
        """Test that nodes with no images are passed through unchanged"""
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_image_non_text_nodes(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, nodes)
    
    def test_split_image_mixed_nodes(self):
        """Test a mix of TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("This is text with ![image](https://example.com/image.png)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("More text with ![another](https://example.com/another.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("bold text", TextType.BOLD),
            TextNode("More text with ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "https://example.com/another.png"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_empty_list(self):
        """Test with empty input list"""
        new_nodes = split_nodes_image([])
        self.assertEqual(new_nodes, [])
    
    def test_split_image_at_start(self):
        """Test image at the start of text"""
        node = TextNode("![image](https://example.com/image.png) at start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode("at end ![image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_only(self):
        """Test text that is entirely an image"""
        node = TextNode("![entire image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("entire image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_multiple_on_same_node(self):
        """Test multiple images in one node"""
        node = TextNode(
            "Start ![img1](https://example.com/img1.png) middle ![img2](https://example.com/img2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/img2.png"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_consecutive(self):
        """Test consecutive images with no text between"""
        node = TextNode(
            "Text ![img1](https://example.com/img1.png)![img2](https://example.com/img2.png) text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode("img2", TextType.IMAGE, "https://example.com/img2.png"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_image_with_complex_alt_text(self):
        """Test image with complex alt text containing spaces and special characters"""
        node = TextNode(
            "Here is ![this is a complex alt text](https://example.com/image.png) image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("this is a complex alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" image", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_basic(self):
        """Test basic link splitting"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_no_links(self):
        """Test that text with no links is passed through unchanged"""
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_link_non_text_nodes(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, nodes)
    
    def test_split_link_mixed_nodes(self):
        """Test a mix of TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("This is text with [link](https://example.com)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("More text with [another link](https://example.com/other)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("bold text", TextType.BOLD),
            TextNode("More text with ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://example.com/other"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_empty_list(self):
        """Test with empty input list"""
        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])
    
    def test_split_link_at_start(self):
        """Test link at the start of text"""
        node = TextNode("[link](https://example.com) at start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode("at end [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_only(self):
        """Test text that is entirely a link"""
        node = TextNode("[entire link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("entire link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_multiple_on_same_node(self):
        """Test multiple links in one node"""
        node = TextNode(
            "Start [link1](https://example1.com) middle [link2](https://example2.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_consecutive(self):
        """Test consecutive links with no text between"""
        node = TextNode(
            "Text [link1](https://example1.com)[link2](https://example2.com) text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example1.com"),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_with_complex_text(self):
        """Test link with complex link text containing spaces and special characters"""
        node = TextNode(
            "Here is [this is a complex link text](https://example.com) link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("this is a complex link text", TextType.LINK, "https://example.com"),
            TextNode(" link", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_split_link_with_special_characters_in_url(self):
        """Test link with special characters in URL"""
        node = TextNode(
            "Visit [boot.dev](https://www.boot.dev?course=backend&lesson=1#section)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://www.boot.dev?course=backend&lesson=1#section"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_textnodes_basic(self):
        """Test with the full example from the assignment"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        # Assert the list matches the expected output

    def test_text_to_textnodes_empty(self):
        """Test with empty string"""
        nodes = text_to_textnodes("")
        # Should return single TEXT node with empty text

    def test_text_to_textnodes_plain_text(self):
        """Test with plain text, no formatting"""
        nodes = text_to_textnodes("Just plain text")
        # Should return single TEXT node

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty_string(self):
        """Test with empty string"""
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_single_block(self):
        """Test with single block (no blank lines)"""
        md = "This is a single paragraph with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no blank lines"])
    
    def test_markdown_to_blocks_multiple_blank_lines(self):
        """Test with multiple consecutive blank lines between blocks"""
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
    
    def test_markdown_to_blocks_only_whitespace(self):
        """Test with only whitespace and blank lines"""
        md = "\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_multiline_block(self):
        """Test block with multiple lines (no blank lines within)"""
        md = "Line 1\nLine 2\nLine 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2\nLine 3"])
    
    def test_markdown_to_blocks_code_block(self):
        """Test with code block (triple backticks)"""
        md = "```\ncode line 1\ncode line 2\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\ncode line 1\ncode line 2\n```"])
    
    def test_markdown_to_blocks_with_headers(self):
        """Test with markdown headers"""
        md = "# Header 1\n\n## Header 2\n\nParagraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Header 1", "## Header 2", "Paragraph"])
    
    def test_markdown_to_blocks_with_formatting(self):
        """Test blocks contain markdown formatting (not parsed into TextNodes)"""
        md = "**bold** and _italic_\n\n`code` and [link](url)"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["**bold** and _italic_", "`code` and [link](url)"]
        )
    
    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        """Test that leading and trailing whitespace is stripped"""
        md = "   Block 1   \n\n   Block 2   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
    
    def test_markdown_to_blocks_indented_lines(self):
        """Test block with indented lines (should strip indentation)"""
        md = "    Line 1\n    Line 2\n    Line 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2\nLine 3"])
    
    def test_markdown_to_blocks_mixed_indentation(self):
        """Test block with mixed indentation levels"""
        md = "  First\n    Second\n  Third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First\nSecond\nThird"])
    
    def test_markdown_to_blocks_list_block(self):
        """Test list as a single block"""
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])
    
    def test_markdown_to_blocks_ordered_list(self):
        """Test ordered list as a single block"""
        md = "1. First\n2. Second\n3. Third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1. First\n2. Second\n3. Third"])
    
    def test_markdown_to_blocks_complex_markdown(self):
        """Test with complex markdown containing multiple element types"""
        md = "# Main Title\n\nThis is a paragraph with **bold**, _italic_, and `code`.\n\n- List item 1\n- List item 2\n- List item 3\n\nAnother paragraph with a [link](https://example.com).\n\n```\nCode block\nwith multiple lines\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Title",
                "This is a paragraph with **bold**, _italic_, and `code`.",
                "- List item 1\n- List item 2\n- List item 3",
                "Another paragraph with a [link](https://example.com).",
                "```\nCode block\nwith multiple lines\n```"
            ]
        )
    
    def test_markdown_to_blocks_blockquote(self):
        """Test blockquote formatting"""
        md = "> Quote line 1\n> Quote line 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["> Quote line 1\n> Quote line 2"])
    
    def test_markdown_to_blocks_multiple_paragraphs_with_blank_lines(self):
        """Test multiple paragraphs separated by blank lines"""
        md = "Para 1\n\nPara 2\n\nPara 3\n\nPara 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Para 1", "Para 2", "Para 3", "Para 4"]
        )
