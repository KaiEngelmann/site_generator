import unittest
from markdown_to_html import markdown_to_html_node, HTMLNode, TextType  # adjust imports


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_heading(self):
        md = "### This is a heading"
        html_tree = markdown_to_html_node(md)
        self.assertEqual(html_tree.children[0].tag, "h3")
        self.assertEqual(len(html_tree.children[0].children), 1)
        self.assertEqual(html_tree.children[0].children[0].value, "This is a heading")

    def test_paragraph_with_inline(self):
        md = "This is **bolded** text and _italic_ text"
        html_tree = markdown_to_html_node(md)
        p = html_tree.children[0]
        self.assertEqual(p.tag, "p")
        tags = [child.tag for child in p.children]
        self.assertIn("b", tags)
        self.assertIn("i", tags)

    def test_code_block(self):
        md = "```\ndef some_code():\n    pass\n```"
        html_tree = markdown_to_html_node(md)
        pre = html_tree.children[0]
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(pre.children[0].tag, "code")
        self.assertIn("def some_code():", pre.children[0].value)

    def test_blockquote(self):
        md = "> This is a quote\n> spanning two lines"
        html_tree = markdown_to_html_node(md)
        blockquote = html_tree.children[0]
        self.assertEqual(blockquote.tag, "blockquote")
        self.assertIn("This is a quote", blockquote.children[0].value)
        self.assertIn("spanning two lines", blockquote.children[1].value)

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        html_tree = markdown_to_html_node(md)
        ol = html_tree.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertEqual(ol.children[0].children[0].value, "First item")

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        html_tree = markdown_to_html_node(md)
        ul = html_tree.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)
        self.assertEqual(ul.children[1].children[0].value, "Second item")

if __name__ == "__main__":
    unittest.main()