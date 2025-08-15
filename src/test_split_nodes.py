from split_nodes_delimiter import *
import unittest
from textnode import *
from textnode import TextType, TextNode



class Test_Split_Nodes(unittest.TestCase):
    def test_backtick_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_asterisk_bold(self):
        node = TextNode("This has *bold* text", TextType.TEXT)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), expected)

    def test_multiple_code_sections(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        # Note: If you want empty text nodes preserved before first code, you could modify expected accordingly.
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ])

    def test_no_delimiter(self):
        node = TextNode("plain text only", TextType.TEXT)
        expected = [TextNode("plain text only", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("Unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
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


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )


        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("Start [first link](https://a.com) ", TextType.TEXT),
            TextNode("Middle text ", TextType.TEXT),
            TextNode("[second link](https://b.com) end", TextType.TEXT),
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://a.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("Middle text ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_images_consecutive(self):
        node = TextNode(
            "Images: ![one](https://img1.png)![two](https://img2.png) done",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("Images: ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://img1.png"),
                TextNode("two", TextType.IMAGE, "https://img2.png"),
                TextNode(" done", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_links_no_links(self):
        node = TextNode("Just plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([node], new_nodes)


    def test_split_images_no_images(self):
        node = TextNode("Text without images.", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual([node], new_nodes)


    def test_split_mixed_nodes(self):
        nodes = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("[link](https://a.com)", TextType.TEXT),
            TextNode(" and ![image](https://img.png)", TextType.TEXT),
            TextNode(" final text.", TextType.TEXT),
        ]
        # First split links, then images
        nodes = split_nodes_links(nodes)
        nodes = split_nodes_images(nodes)
        
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://img.png"),
                TextNode(" final text.", TextType.TEXT),
            ],
            nodes,
        )

    def test_plain_text(self):
            text = "Just some plain text."
            nodes = text_to_textnodes(text)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].text, "Just some plain text.")
            self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_bold_text(self):
        text = "This is **bold** text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_italic_and_code(self):
        text = "This has _italic_ and `code`."
        nodes = text_to_textnodes(text)
        italic_node = [n for n in nodes if n.text_type == TextType.ITALIC][0]
        code_node = [n for n in nodes if n.text_type == TextType.CODE][0]
        self.assertEqual(italic_node.text, "italic")
        self.assertEqual(code_node.text, "code")

    def test_image_and_link(self):
        text = "Here is an ![image](https://example.com/image.png) and a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        image_node = [n for n in nodes if n.text_type == TextType.IMAGE][0]
        link_node = [n for n in nodes if n.text_type == TextType.LINK][0]
        self.assertEqual(image_node.text, "image")
        self.assertEqual(image_node.url, "https://example.com/image.png")
        self.assertEqual(link_node.text, "link")
        self.assertEqual(link_node.url, "https://example.com")

    def test_no_empty_nodes(self):
        text = "This is **bold**."
        nodes = text_to_textnodes(text)
        for node in nodes:
            self.assertNotEqual(node.text, "")
    


    


if __name__ == "__main__":
    unittest.main()
