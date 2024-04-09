from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html
from inline import text_to_textnodes, TextNode
from enum import Enum
import re


class BlockType(Enum):
    BLOCK_TYPE_PARAGRAPH = "paragraph"
    BLOCK_TYPE_HEADER = "header"
    BLOCK_TYPE_QUOTE = "quote"
    BLOCK_TYPE_CODE = "code"
    BLOCK_TYPE_ULIST = "unordered_list"
    BLOCK_TYPE_OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]


def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split("\n")
    if re.match(r"^(#{1,6})\s", block):
        return BlockType.BLOCK_TYPE_HEADER
    if re.match(r"^```[^`]+```$", block):
        return BlockType.BLOCK_TYPE_CODE
    if re.match(r"^>\s", block):
        for line in lines:
            if re.match(r"^>\s", line):
                return BlockType.BLOCK_TYPE_QUOTE
            return BlockType.BLOCK_TYPE_PARAGRAPH
    if re.match(r"^[*-]\s", block):
        for line in lines:
            if re.match(r"^[*-]\s", line):
                return BlockType.BLOCK_TYPE_ULIST
            return BlockType.BLOCK_TYPE_PARAGRAPH
        return BlockType.BLOCK_TYPE_ULIST
    if re.match(r"^\d+\.\s", block):
        for line in lines:
            if re.match(r"^\d+\.\s", line):
                return BlockType.BLOCK_TYPE_OLIST
        return BlockType.BLOCK_TYPE_PARAGRAPH
    return BlockType.BLOCK_TYPE_PARAGRAPH


def header_block_to_htmlnode(block: str) -> ParentNode:
    header_level: int = len(block) - len(block.lstrip("#"))
    children_nodes: list[HTMLNode] = text_to_children(block.lstrip("#").strip())
    return ParentNode(tag=f"h{header_level}", children=children_nodes)


def code_block_to_htmlnode(block: str) -> ParentNode:
    children_nodes: list[HTMLNode] = text_to_children(
        block.lstrip("```").rstrip("```").strip()
    )
    code_parentnode: ParentNode = ParentNode(tag="code", children=children_nodes)
    return ParentNode(tag="pre", children=[code_parentnode])


def quote_block_to_htmlnode(block: str) -> HTMLNode:
    lines: list[str] = block.split("\n")
    new_lines: list[str] = [
        line.lstrip(">").strip() for line in lines if re.match(r"^> ", line)
    ]
    content: str = " ".join(new_lines)
    children_nodes: list[HTMLNode] = text_to_children(content)
    return ParentNode(tag="blockquote", children=children_nodes)


def unordered_list_block_to_htmlnode(block: str) -> HTMLNode:
    items: list[str] = block.split("\n")
    html_items: list[HTMLNode] = []
    for item in items:
        text: str = item.lstrip("-* ")
        children_nodes: list[HTMLNode] = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children_nodes))
    return ParentNode(tag="ul", children=html_items)


def ordered_list_block_to_htmlnode(block: str) -> HTMLNode:
    items: list[str] = block.split("\n")
    html_items: list[HTMLNode] = []
    for item in items:
        text: str = item[3:].strip()
        children_nodes: list[HTMLNode] = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children_nodes))
    return ParentNode(tag="ol", children=html_items)


def paragraph_block_to_htmlnode(block: str) -> ParentNode:
    lines: list[str] = block.split("\n")
    paragraph: str = " ".join(lines)
    children_nodes: list[HTMLNode] = text_to_children(paragraph)
    return ParentNode(tag="p", children=children_nodes)


def block_to_htmlnode(block: str) -> HTMLNode:
    block_type: BlockType = block_to_block_type(block)
    if block_type == BlockType.BLOCK_TYPE_HEADER:
        return header_block_to_htmlnode(block)
    if block_type == BlockType.BLOCK_TYPE_CODE:
        return code_block_to_htmlnode(block)
    if block_type == BlockType.BLOCK_TYPE_QUOTE:
        return quote_block_to_htmlnode(block)
    if block_type == BlockType.BLOCK_TYPE_ULIST:
        return unordered_list_block_to_htmlnode(block)
    if block_type == BlockType.BLOCK_TYPE_OLIST:
        return ordered_list_block_to_htmlnode(block)
    return paragraph_block_to_htmlnode(block)


def markdown_to_htmlnode(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    children_nodes: list[HTMLNode] = []
    for block in blocks:
        htmlnode: HTMLNode = block_to_htmlnode(block)
        children_nodes.append(htmlnode)

    return ParentNode(tag="div", children=children_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    # convert inline markdown (bold, italic, code) to text nodes
    text_nodes: list[TextNode] = text_to_textnodes(text)
    return [text_node_to_html(node) for node in text_nodes]
