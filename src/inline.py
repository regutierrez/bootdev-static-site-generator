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


def extract_markdown_images(text: str) -> list[tuple] | None:
    image_re: str = r"\!\[(.*?)\]\((.*?)\)"
    matches: list[tuple] = re.findall(image_re, text)
    if len(matches) == 0:
        return None
    return matches


def extract_markdown_links(text: str) -> list[tuple] | None:
    link_re: str = r"\[(.*?)\]\((.*?)\)"
    matches: list[tuple] = re.findall(link_re, text)
    if len(matches) == 0:
        return None
    return matches


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        matches: list[tuple] | None = extract_markdown_images(node.text)
        if matches is None:
            new_nodes.append(node)
            continue
        node_text: str = node.text
        for match in matches:
            sections: list[str] = node_text.split(f"![{match[0]}]({match[1]})", 1)
            if len(sections) <= 1:
                continue
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_image, match[1]))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        matches: list[tuple] | None = extract_markdown_links(node.text)
        if matches is None:
            new_nodes.append(node)
            continue
        node_text: str = node.text
        for match in matches:
            sections: list[str] = node_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) <= 1:
                continue
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(match[0], text_type_link, match[1]))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes: list[TextNode] = [TextNode(text, text_type_text)]
    delimiter_dict: dict[str, str] = {
        "**": text_type_bold,
        "*": text_type_italic,
        "`": text_type_code,
    }

    for delimiter, text_type in delimiter_dict.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)

    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)

    return new_nodes
