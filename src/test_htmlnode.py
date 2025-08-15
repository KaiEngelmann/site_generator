import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):

    def test1(self):
        node1 = HTMLNode(tag="a", value="Click", props={"href": "https://example.com"})
        repr_str = repr(node1)
        assert "tag='a'" in repr_str
        assert "value='Click'" in repr_str
        assert "props={'href': 'https://example.com'}" in repr_str
        


    def test_2(self):
        node1 = HTMLNode(tag="a", value="Click", props={"href": "https://example.com"})
        print(node1.props_to_html())
        assert node1.props_to_html() == ' href="https://example.com"'

    def test_3(self):
        node3 = HTMLNode(tag="p", value="Hello")
        assert node3.props_to_html() == ""

    def test_4(self):
        node4 = HTMLNode(tag="div")
        assert node4.children == None

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode_basic_html(self):
        node = LeafNode("p", "Hello world")
        assert node.to_html() == "<p>Hello world</p>"

    def test_leafnode_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com", "target": "_blank"})
        assert node.to_html() == '<a href="https://example.com" target="_blank">Click here</a>'

    def test_leafnode_no_tag_returns_raw_text(self):
        node = LeafNode(None, "Just text")
        assert node.to_html() == "Just text"

    def test_leafnode_raises_if_no_value(self):
        try:
            LeafNode("p", None).to_html()
            assert False, "Expected ValueError for missing value"
        except ValueError:
            pass


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )

    def test_to_html_nested_three_levels(self):
        deep_child = LeafNode("i", "deep")
        middle_child = ParentNode("span", [deep_child])
        top_parent = ParentNode("section", [middle_child])
        self.assertEqual(
            top_parent.to_html(),
            "<section><span><i>deep</i></span></section>",
        )

if __name__ == "__main__":
    unittest.main()