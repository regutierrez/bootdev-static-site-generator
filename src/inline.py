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


node = TextNode("This is text with a *code block* word", text_type_text)
# node = TextNode("This is text with a code block word", text_type_text)
new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

print(new_nodes)
