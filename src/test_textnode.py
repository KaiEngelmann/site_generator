import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_property(self):
        node = TextNode("text1", TextType.ITALIC)
        node2 = TextNode("text1", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("text1", TextType.ITALIC, url="sam.url")
        node2 = TextNode("text1", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
