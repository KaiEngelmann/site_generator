from enum import Enum
import re


document = """ # This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        new_blocks.append(block.strip())
    return new_blocks






class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    if re.match(r"^(>\s?.*\n?)+$", block):
        return BlockType.QUOTE
    if re.match(r"^(- .*\n?)+$", block):
        return BlockType.UNORDERED_LIST
    if re.match(r"^(\d+\. .*\n?)+$", block):
        lines = block.split("\n")
        for i, line in enumerate(lines, start=1):
            match = re.match(r"^(\d+)\. ", line)
            if not match or int(match.group(1)) != i:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH



def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match(r"^# ", block):
            match = block[1:]
            return match.strip()

        
    else:
        raise Exception("No h1 header")
