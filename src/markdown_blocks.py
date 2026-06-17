import re
from enum import Enum
from utils import markdown_to_blocks

class MarkdownBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    heading_pattern = r"^(#{1,6})\s+.*$"
    if re.match(heading_pattern, block):
        return MarkdownBlockType.HEADING

    code_pattern = r"^```.*\n[\s\S]*\n```$"
    if re.match(code_pattern, block):
        return MarkdownBlockType.CODE

    quote_pattern = r"^(> ?.*\n)*> ?.*$"
    if re.match(quote_pattern, block):
        return MarkdownBlockType.QUOTE

    unordered_list_pattern = r"^(- .*\n)*- .*$"
    if re.match(unordered_list_pattern, block):
        return MarkdownBlockType.UNORDERED_LIST

    ordered_list_pattern = r"^\d+\. .*(\n\d+\. .*)*$"
    if re.match(ordered_list_pattern, block):
        return MarkdownBlockType.ORDERED_LIST
    
    return MarkdownBlockType.PARAGRAPH