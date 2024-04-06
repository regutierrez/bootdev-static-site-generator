import unittest
from blocks import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
