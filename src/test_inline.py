import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html,
)

from inline import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode(
            "This is text with a `code block` word", TextType.TEXT_TYPE_TEXT.value
        )
        result = [
            TextNode("This is text with a ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("code block", TextType.TEXT_TYPE_CODE.value),
            TextNode(" word", TextType.TEXT_TYPE_TEXT.value),
        ]

        self.assertEqual(
            split_nodes_delimiter(
                [node],
                "`",
                TextType.TEXT_TYPE_CODE.value,
            ),
            result,
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(extract_markdown_images(text), result)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(extract_markdown_links(text), result)

    def test_split_nodes_images_no_images(self):
        nodes = [
            TextNode("This is text without any images.", TextType.TEXT_TYPE_TEXT.value)
        ]
        expected = [
            TextNode("This is text without any images.", TextType.TEXT_TYPE_TEXT.value)
        ]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_images_single_image(self):
        nodes = [
            TextNode(
                "This is text with an ![image](http://example.com/image.png).",
                TextType.TEXT_TYPE_TEXT.value,
            )
        ]
        expected = [
            TextNode("This is text with an ", TextType.TEXT_TYPE_TEXT.value),
            TextNode(
                "image", TextType.TEXT_TYPE_IMAGE.value, "http://example.com/image.png"
            ),
            TextNode(".", TextType.TEXT_TYPE_TEXT.value),
        ]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_images_multiple_images(self):
        nodes = [
            TextNode(
                "![img1](http://example.com/img1.png) Text ![img2](http://example.com/img2.png)",
                TextType.TEXT_TYPE_TEXT.value,
            )
        ]
        expected = [
            TextNode(
                "img1", TextType.TEXT_TYPE_IMAGE.value, "http://example.com/img1.png"
            ),
            TextNode(" Text ", TextType.TEXT_TYPE_TEXT.value),
            TextNode(
                "img2", TextType.TEXT_TYPE_IMAGE.value, "http://example.com/img2.png"
            ),
        ]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_links_no_links(self):
        nodes = [
            TextNode("This is text without any links.", TextType.TEXT_TYPE_TEXT.value)
        ]
        expected = [
            TextNode("This is text without any links.", TextType.TEXT_TYPE_TEXT.value)
        ]
        self.assertEqual(split_nodes_links(nodes), expected)

    def test_split_nodes_links_single_link(self):
        nodes = [
            TextNode(
                "This is text with an [link](https://www.example.com).",
                TextType.TEXT_TYPE_TEXT.value,
            )
        ]
        expected = [
            TextNode("This is text with an ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("link", TextType.TEXT_TYPE_LINK.value, "https://www.example.com"),
            TextNode(".", TextType.TEXT_TYPE_TEXT.value),
        ]
        self.assertEqual(split_nodes_links(nodes), expected)

    def test_split_nodes_links_multiple_links(self):
        nodes = [
            TextNode(
                "This is text with [link1](https://www.example.com) and [link2](https://www.example.com/another).",
                TextType.TEXT_TYPE_TEXT.value,
            )
        ]
        expected = [
            TextNode("This is text with ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("link1", TextType.TEXT_TYPE_LINK.value, "https://www.example.com"),
            TextNode(" and ", TextType.TEXT_TYPE_TEXT.value),
            TextNode(
                "link2",
                TextType.TEXT_TYPE_LINK.value,
                "https://www.example.com/another",
            ),
            TextNode(".", TextType.TEXT_TYPE_TEXT.value),
        ]
        self.assertEqual(split_nodes_links(nodes), expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("text", TextType.TEXT_TYPE_BOLD.value),
            TextNode(" with an ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("italic", TextType.TEXT_TYPE_ITALIC.value),
            TextNode(" word and a ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("code block", TextType.TEXT_TYPE_CODE.value),
            TextNode(" and an ", TextType.TEXT_TYPE_TEXT.value),
            TextNode(
                "image",
                TextType.TEXT_TYPE_IMAGE.value,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("link", TextType.TEXT_TYPE_LINK.value, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), result)

    def test_text_to_textnodes_adjacent_delimiters(self):
        # Test with adjacent delimiters (bold text immediately followed by italic text)
        text = "**bold****italic**"
        result = [
            TextNode("bold", TextType.TEXT_TYPE_BOLD.value),
            TextNode("italic", TextType.TEXT_TYPE_BOLD.value),
        ]
        self.assertEqual(text_to_textnodes(text), result)

    def test_text_to_textnodes_no_markdown(self):
        # Test with no markdown elements at all
        text = "Just plain text with no special formatting."
        result = [
            TextNode(
                "Just plain text with no special formatting.",
                TextType.TEXT_TYPE_TEXT.value,
            ),
        ]
        self.assertEqual(text_to_textnodes(text), result)

    def test_text_to_textnodes_multiple_images_and_links(self):
        # Test with multiple images and links interspersed with text
        text = "Text with ![img1](http://img1.png) and [link1](http://link1) plus ![img2](http://img2.png) and [link2](http://link2)"
        result = [
            TextNode("Text with ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("img1", TextType.TEXT_TYPE_IMAGE.value, "http://img1.png"),
            TextNode(" and ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("link1", TextType.TEXT_TYPE_LINK.value, "http://link1"),
            TextNode(" plus ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("img2", TextType.TEXT_TYPE_IMAGE.value, "http://img2.png"),
            TextNode(" and ", TextType.TEXT_TYPE_TEXT.value),
            TextNode("link2", TextType.TEXT_TYPE_LINK.value, "http://link2"),
        ]
        self.assertEqual(text_to_textnodes(text), result)


if __name__ == "__main__":
    unittest.main()
