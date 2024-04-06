import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html,
)

from inline import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
)


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), result)

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
        nodes = [TextNode("This is text without any images.", text_type_text)]
        expected = [TextNode("This is text without any images.", text_type_text)]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_images_single_image(self):
        nodes = [
            TextNode(
                "This is text with an ![image](http://example.com/image.png).",
                text_type_text,
            )
        ]
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "http://example.com/image.png"),
            TextNode(".", text_type_text),
        ]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_images_multiple_images(self):
        nodes = [
            TextNode(
                "![img1](http://example.com/img1.png) Text ![img2](http://example.com/img2.png)",
                text_type_text,
            )
        ]
        expected = [
            TextNode("img1", text_type_image, "http://example.com/img1.png"),
            TextNode(" Text ", text_type_text),
            TextNode("img2", text_type_image, "http://example.com/img2.png"),
        ]
        self.assertEqual(split_nodes_images(nodes), expected)

    def test_split_nodes_links_no_links(self):
        nodes = [TextNode("This is text without any links.", text_type_text)]
        expected = [TextNode("This is text without any links.", text_type_text)]
        self.assertEqual(split_nodes_links(nodes), expected)

    def test_split_nodes_links_single_link(self):
        nodes = [
            TextNode(
                "This is text with an [link](https://www.example.com).", text_type_text
            )
        ]
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(".", text_type_text),
        ]
        self.assertEqual(split_nodes_links(nodes), expected)

    def test_split_nodes_links_multiple_links(self):
        nodes = [
            TextNode(
                "This is text with [link1](https://www.example.com) and [link2](https://www.example.com/another).",
                text_type_text,
            )
        ]
        expected = [
            TextNode("This is text with ", text_type_text),
            TextNode("link1", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("link2", text_type_link, "https://www.example.com/another"),
            TextNode(".", text_type_text),
        ]
        self.assertEqual(split_nodes_links(nodes), expected)


if __name__ == "__main__":
    unittest.main()
