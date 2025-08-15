import unittest
from markdown_to_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
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


    def test_markdown_blocks2(self):
        md = """
This is a [link](url) with a ![image]

 and some more crap here    

   and some _italic_ maybe   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a [link](url) with a ![image]",
                "and some more crap here",
                "and some _italic_ maybe",
            ],
        )


    def test_check_block(self):
        block = """1. First item
2. Second item
3. Third item
4. Fourth item"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.ORDERED_LIST
        )
    def test_check_block2(self):
        block = """- 1. First item
- 2. Second item
- 4. Third item
- 3. Fourth item"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.UNORDERED_LIST
        )
    def test_check_block3(self):
        block = """``` (a bunch)
        of code
        x = 23```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.CODE
        )

    def test_check_block4(self):
        block = """#### this is a heading"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.HEADING
        )
    
    def test_check_block5(self):
        block = """>this
> is
>    a
>quote"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type, BlockType.QUOTE
        )
    



if __name__ == "__main__":
    unittest.main()