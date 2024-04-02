import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html,
    text_type_bold,
    text_type_italic,
)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes: list[TextNode] = []
        texts: list[str] = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            new_nodes.append(node)
        else:
            for count in range(len(texts)):
                if texts[count] == "":
                    continue
                if count % 2 == 0:
                    split_nodes.append(TextNode(texts[count], text_type_text))
                else:
                    split_nodes.append(TextNode(texts[count], text_type))
            new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    image_re: str = r"\!\[(.*?)\]\((.*?)\)"
    matches: list[tuple] = re.findall(image_re, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    link_re: str = r"\[(.*?)\]\((.*?)\)"
    matches: list[tuple] = re.findall(link_re, text)

    return matches


# test for extract_markdown_images
text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
print(extract_markdown_images(text))
# [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

# test for extract_markdown_links
text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
print(extract_markdown_links(text))
# [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]


# node = TextNode("This is text with a *code block* word", text_type_text)
# node = TextNode("This is text with a code block word", text_type_text)
# new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
# print(new_nodes)
