from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode
from text_to_html import text_node_to_html_node
from split_nodes_delimiter import text_to_textnodes
from textnode import TextNode, TextType
import re


Jasmine = """
##### **Flowers** are _cool_

1. roses
2. tulips
3. sunflowers 

```
def flowers(self):
    for flower in flowers:
        return flower
```


"""

md = """
### This is a heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
def some random code
```

>    this is a quote

1. this is
2. an ordered
3. list

"""

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    full_doc = HTMLNode(tag='div', children=child_nodes)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6}) (.*)$", block)
            hashes, text = match.groups()
            level = len(hashes)
            tag = f"h{level}"
            children = text_to_children(text)
            child_nodes.append(HTMLNode(tag=tag, children=children))
        elif block_type == BlockType.QUOTE:
            li_children = []
            for line in block.splitlines():
                if len(line) > 1:
                    content = line[1:] if line[1] != " " else line[2:]
                else:
                    content = ""
                li_children.extend(text_to_children(content))
            child_nodes.append(HTMLNode(tag="blockquote", children=li_children))
        elif block_type == BlockType.CODE:
            stripped = block[3:-3].strip("\n")
            code_node = TextNode(text=stripped, text_type=TextType.CODE)
            code_html = text_node_to_html_node(code_node)
            child_nodes.append(HTMLNode(tag="pre", children=[code_html]))
        elif block_type == BlockType.ORDERED_LIST:
            list_nodes = []
            for line in block.splitlines():
                ordered_list = line[3:]
                children = text_to_children(ordered_list)
                list_nodes.append(HTMLNode(tag="li", children=children))
            child_nodes.append(HTMLNode(tag="ol", children=list_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            list_nodes = []
            for line in block.splitlines():
                unordered_list = line[2:]
                children = text_to_children(unordered_list)
                list_nodes.append(HTMLNode(tag="li", children=children))
            child_nodes.append(HTMLNode(tag="ul", children=list_nodes))
                
        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            child_nodes.append(HTMLNode(tag="p", children=children))

    return full_doc

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]

    return html_nodes

def render_html_node(node):
    if isinstance(node, LeafNode):
        if node.tag is None:
            return node.value
        if node.tag == "img":
            props = " ".join(f'{k}="{v}"' for k, v in node.props.items())
            return f"<img {props} />"
        if node.tag == "a":
            href = node.props.get("href", "#")
            return f'<a href="{href}">{node.value}</a>'
        return f"<{node.tag}>{node.value}</{node.tag}>"
    elif isinstance(node, HTMLNode):
        children_html = "".join(render_html_node(child) for child in node.children)
        return f"<{node.tag}>{children_html}</{node.tag}>"
    else:
        raise TypeError("Unknown node type")



html_tree = markdown_to_html_node(md)
html_string = render_html_node(html_tree)


html_tree = markdown_to_html_node(Jasmine)
html_string = render_html_node(html_tree)
