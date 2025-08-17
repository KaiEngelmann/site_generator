import os
from markdown_to_html import markdown_to_html_node, render_html_node
from markdown_to_blocks import extract_title



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_file = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_file = f.read()
    html_tree = markdown_to_html_node(markdown_file)
    html_string = render_html_node(html_tree)
    title = extract_title(markdown_file)
    filled_template = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
            f.write(filled_template)
    




