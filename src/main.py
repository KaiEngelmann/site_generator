from textnode import TextType, TextNode
import os
from copystatic import copy_contents
from generate_path import generate_page

def main():
	
	node = TextNode("text", TextType.LINK, "somelink.com")
	formatted = node.text_type.value.format(text=node.text, url=node.url)

	copy_contents("/mnt/d/site_generator/static", "/mnt/d/site_generator/public")
	markdown_file = "/mnt/d/site_generator/content/index.md"
	template = "/mnt/d/site_generator/template.html"
	destination = "/mnt/d/site_generator/public/index.html"
	generate_page(markdown_file, template, destination)







if __name__ == "__main__":


	main()
