import unittest
from regex import extract_markdown_images, extract_markdown_links
class Test_Regex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_alt_text_with_special_characters(self):
        matches = extract_markdown_images(
            "Here is ![alt text with !@#$%^&*()_+ symbols](https://example.com/img.png)"
        )
        self.assertListEqual([
            ("alt text with !@#$%^&*()_+ symbols", "https://example.com/img.png")
        ], matches)

    def test_spaces_in_markdown_syntax(self):
        matches = extract_markdown_images(
            "![ spaced alt   ](   https://example.com/spaces.png   )"
        )
        # Depending on whether you strip() inside your function, this may need trimming
        self.assertListEqual([
            (" spaced alt   ", "   https://example.com/spaces.png   ")
        ], matches)

    def test_missing_alt_text(self):
        matches = extract_markdown_images(
            "![](https://example.com/no-alt.png)"
        )
        self.assertListEqual([
            ("", "https://example.com/no-alt.png")
        ], matches)

    def test_no_matches(self):
        matches = extract_markdown_images(
            "This has no images at all."
        )
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()