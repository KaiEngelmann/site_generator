from textnode import TextType, TextNode
import os
from copystatic import copy_contents
from generate_path import generate_pages_recursive

def main():
	
	node = TextNode("text", TextType.LINK, "somelink.com")
	formatted = node.text_type.value.format(text=node.text, url=node.url)

	current_script_dir = os.path.dirname(os.path.abspath(__file__))

	project_root = os.path.dirname(current_script_dir)

	static_path = os.path.join(project_root, "static")
	public_path = os.path.join(project_root, "public")
	content_index_path = os.path.join(project_root, "content")
	template = os.path.join(project_root, "template.html")
	content_destination = os.path.join(public_path)


	copy_contents(static_path, public_path)
	generate_pages_recursive(content_index_path, template, content_destination)





if __name__ == "__main__":


	main()
