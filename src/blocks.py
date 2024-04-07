from enum import Enum
import re


class BlockType(Enum):
    BLOCK_TYPE_PARAGRAPH = "paragraph"
    BLOCK_TYPE_HEADER = "header"
    BLOCK_TYPE_QUOTE = "quote"
    BLOCK_TYPE_CODE = "code"
    BLOCK_TYPE_ULIST = "unordered_list"
    BLOCK_TYPE_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    return [block.strip() for block in text.split("\n\n") if block.strip() != ""]


def block_to_block_type(block: str) -> str:
    if re.match(r"^(#{1,6})\s", block):
        return BlockType.BLOCK_TYPE_HEADER.value
    if re.match(r"^```[^`]+```$", block):
        return BlockType.BLOCK_TYPE_CODE.value
    if re.match(r"^>\s", block):
        return BlockType.BLOCK_TYPE_QUOTE.value
    if re.match(r"^[*-]\s", block):
        return BlockType.BLOCK_TYPE_ULIST.value
    if re.match(r"^\d+\.\s", block):
        return BlockType.BLOCK_TYPE_LIST.value
    return BlockType.BLOCK_TYPE_PARAGRAPH.value
