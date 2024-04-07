import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks("test"), ["test"])

    def test_markdown_to_blocks_with_weird_spacing(self):
        test = """
 This is **bolded** paragraph

    
 

 This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
 * with items
 
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n * with items",
        ]
        self.assertEqual(markdown_to_blocks(test), expected)

    def test_headers(self):
        self.assertEqual(
            block_to_block_type("### test"), BlockType.BLOCK_TYPE_HEADER.value
        )
        self.assertEqual(
            block_to_block_type("# test"), BlockType.BLOCK_TYPE_HEADER.value
        )
        self.assertEqual(
            block_to_block_type("###### test"), BlockType.BLOCK_TYPE_HEADER.value
        )
        self.assertEqual(
            block_to_block_type("########### test"),
            BlockType.BLOCK_TYPE_PARAGRAPH.value,
        )

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```code```"), BlockType.BLOCK_TYPE_CODE.value
        )
        self.assertEqual(
            block_to_block_type("```\nmulti-line code\n```"),
            BlockType.BLOCK_TYPE_CODE.value,
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> quote"), BlockType.BLOCK_TYPE_QUOTE.value
        )
        self.assertEqual(
            block_to_block_type(">quote"), BlockType.BLOCK_TYPE_PARAGRAPH.value
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item"), BlockType.BLOCK_TYPE_ULIST.value
        )
        self.assertEqual(
            block_to_block_type("* item"), BlockType.BLOCK_TYPE_ULIST.value
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. item"), BlockType.BLOCK_TYPE_LIST.value
        )
        self.assertEqual(
            block_to_block_type("2 item"), BlockType.BLOCK_TYPE_PARAGRAPH.value
        )
        self.assertEqual(
            block_to_block_type("10. item"), BlockType.BLOCK_TYPE_LIST.value
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph."),
            BlockType.BLOCK_TYPE_PARAGRAPH.value,
        )
        self.assertEqual(block_to_block_type(""), BlockType.BLOCK_TYPE_PARAGRAPH.value)


if __name__ == "__main__":
    unittest.main()
