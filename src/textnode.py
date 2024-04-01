from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


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
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html(textnode: TextNode) -> LeafNode:
    if textnode.text_type == text_type_text:
        return LeafNode(None, textnode.text)
    elif textnode.text_type == text_type_bold:
        return LeafNode("b", textnode.text)
    elif textnode.text_type == text_type_italic:
        return LeafNode("i", textnode.text)
    elif textnode.text_type == text_type_code:
        return LeafNode("code", textnode.text)
    elif textnode.text_type == text_type_link:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    elif textnode.text_type == text_type_image:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
    else:
        raise ValueError
