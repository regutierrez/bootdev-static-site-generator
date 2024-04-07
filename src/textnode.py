from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT_TYPE_TEXT = "text"
    TEXT_TYPE_BOLD = "bold"
    TEXT_TYPE_ITALIC = "italic"
    TEXT_TYPE_CODE = "code"
    TEXT_TYPE_LINK = "link"
    TEXT_TYPE_IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: str = text_type
        self.url: str | None = url

    def __eq__(self, other) -> bool:
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self) -> str:
        if self.url is None:
            return f"TextNode({self.text}, {self.text_type})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html(textnode: TextNode) -> LeafNode:
    if textnode.text_type == TextType.TEXT_TYPE_TEXT.value:
        return LeafNode(None, textnode.text)
    elif textnode.text_type == TextType.TEXT_TYPE_BOLD.value:
        return LeafNode("b", textnode.text)
    elif textnode.text_type == TextType.TEXT_TYPE_ITALIC.value:
        return LeafNode("i", textnode.text)
    elif textnode.text_type == TextType.TEXT_TYPE_CODE.value:
        return LeafNode("code", textnode.text)
    elif textnode.text_type == TextType.TEXT_TYPE_LINK.value:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    elif textnode.text_type == TextType.TEXT_TYPE_IMAGE.value:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
    else:
        raise ValueError("invalid text type")
