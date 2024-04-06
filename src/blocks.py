def markdown_to_blocks(text: str) -> list[str]:
    blocks: list[str] = text.split("\n\n")

    return blocks


test = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

print(markdown_to_blocks(test))
