from textnode import TextType, TextNode

def main():
	
	node = TextNode("text", TextType.LINK, "somelink.com")
	formatted = node.text_type.value.format(text=node.text, url=node.url)
	print(formatted)


if __name__ == "__main__":


	main()
