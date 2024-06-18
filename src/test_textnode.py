import unittest

from textnode import TextNode, TextType, text_node_to_html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT_TYPE_TEXT.value)
        node2 = TextNode("This is a text node", TextType.TEXT_TYPE_TEXT.value)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT_TYPE_TEXT.value)
        node2 = TextNode("This is a text node", TextType.TEXT_TYPE_BOLD.value)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT_TYPE_TEXT.value)
        node2 = TextNode("This is a text node2", TextType.TEXT_TYPE_TEXT.value)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT_TYPE_ITALIC.value,
            "https://www.boot.dev",
        )
        node2 = TextNode(
            "This is a text node",
            TextType.TEXT_TYPE_ITALIC.value,
            "https://www.boot.dev",
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "This is a text node", TextType.TEXT_TYPE_TEXT.value, "https://www.boot.dev"
        )
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text_node_to_html(self):
        node = text_node_to_html(
            TextNode(
                "This is a text node",
                TextType.TEXT_TYPE_IMAGE.value,
                "https://www.boot.dev",
            )
        )
        print(node.to_html())
        self.assertEqual(
            node.to_html(),
            '<img src="https://www.boot.dev" alt="This is a text node"></img>',
        )


if __name__ == "__main__":
    unittest.main()
