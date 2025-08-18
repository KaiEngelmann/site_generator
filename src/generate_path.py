import os
from markdown_to_html import markdown_to_html_node, render_html_node
from markdown_to_blocks import extract_title
from pathlib import Path



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_file = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_file = f.read()
    html_tree = markdown_to_html_node(markdown_file)
    html_string = render_html_node(html_tree)
    title = extract_title(markdown_file)
    filled_template = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    if not basepath.endswith("/"):
        basepath += "/"
    filled_template = filled_template.replace('href="/', f'href="{basepath}')
    filled_template = filled_template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
            f.write(filled_template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_root = Path(dir_path_content)
    template = Path(template_path)
    dest_root = Path(dest_dir_path)

    def crawl(content_dir, dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

        for name in os.listdir(content_dir):
            content_path = os.path.join(content_dir, name)
            dest_path = os.path.join(dest_dir, name)

            if os.path.isfile(content_path):
                if name.endswith(".md"):
                    dest_html_path = str(Path(dest_path).with_suffix(".html"))
                    generate_page(content_path, str(template), dest_html_path, basepath)
            else:
                crawl(content_path, dest_path)
    crawl(str(content_root), str(dest_root))
                