from regex import extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Unmatched delimiter")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                    new_nodes.append(TextNode(part, text_type))
        
    return new_nodes

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        for anchor, link, in links:
            before_text, after_text = text.split(f"[{anchor}]({link})", 1)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, link))
            text = after_text
        if text:
            new_nodes.append(TextNode(after_text, TextType.TEXT))
    return new_nodes

        


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        for image_alt, image_link in images:
            before_text, after_text = text.split(f"![{image_alt}]({image_link})", 1)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = after_text
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes



