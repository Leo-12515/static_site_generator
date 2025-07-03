import unittest
from extract import markdown_to_blocks, markdown_to_html_node
from utils import extract_markdown_images, extract_markdown_links
from main import extract_title

class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with several images, ![image](https://i.imgur.com/zjjcJKZ.png), ![image duck](https://i.imgur.com/duck.png), ![image plane](https://i.imgur.com/plane.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image duck", "https://i.imgur.com/duck.png"), ("image plane", "https://i.imgur.com/plane.png")], matches)

    def test_extract_mark_down_links(self):
        matches = extract_markdown_links(
            "This is text with an [link name](https://www.youtube.com/channel)"
        )
        self.assertListEqual([("link name", "https://www.youtube.com/channel")], matches)

    def test_extract_mark_down_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with several links, [link name](https://www.youtube.com/channel), [link google](https://www.google.com/softwarecourses), [link personal](https://www.mysite.com/summary)"
        )
        self.assertListEqual([("link name", "https://www.youtube.com/channel"), ("link google","https://www.google.com/softwarecourses"), ("link personal","https://www.mysite.com/summary")], matches)

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an no image"
        )
        self.assertListEqual([], matches)

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with an no link"
        )
        self.assertListEqual([], matches)

    def test_extract_image_mixed_in_links(self):
        matches = extract_markdown_images(
            "This is text with several links, [link name](https://www.youtube.com/channel), ![image](https://i.imgur.com/zjjcJKZ.png), [link personal](https://www.mysite.com/summary)"
        )
        self.assertListEqual([("image","https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_link_mixed_in_images(self):
        matches = extract_markdown_links(
            "This is text with several links, ![image](https://i.imgur.com/zjjcJKZ.png), [link name](https://www.youtube.com/channel),  ![image plane](https://i.imgur.com/plane.png)"
        )
        self.assertListEqual([("link name","https://www.youtube.com/channel")], matches)
    
    def test_extract_title(self):
        md = "# This is a title\n\nThis is some content."
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_first_line(self):
        md = " \n\nThis is some content."
        # This is where you tell the test to *expect* an exception
        with self.assertRaises(Exception): 
            # And this is the code that *should* raise the exception
            extract_title(md) 

    def test_extract_title_empty_markdown(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_extract_title_wrong_markdown(self):
        md = "## This is not a title\n\nThis is some content."
        with self.assertRaises(Exception):
            extract_title(md)



class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_different_types_of_blocks(self):
        md = """
# This is a header

```this is a code block```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "# This is a header",
            "```this is a code block```",
        ],
    )
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
        
    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a single line of text without newlines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line of text without newlines."])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "This is a line.\n\n\nThis is another line."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a line.", "This is another line."])
    
    def test_markdown_to_blocks_trailing_newlines(self):
        md = "This is a line.\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a line."])

    def test_markdown_to_blocks_leading_newlines(self):
        md = "\n\nThis is a line."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a line."])

    def test_markdown_to_blocks_mixed_content(self):
        md = """
This is a line with **bold text** and _italic text_.

This is a line with `inline code`.

This is a line with a [link](https://example.com). 

This is a line with an ![image](https://example.com/image.png).
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a line with **bold text** and _italic text_.",
                "This is a line with `inline code`.",
                "This is a line with a [link](https://example.com).",
                "This is a line with an ![image](https://example.com/image.png)."
            ]
        )

    def test_markdown_to_blocks_no_content(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    def test_markdown_to_blocks_single_newline(self):
        md = "\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    def test_markdown_to_blocks_multiple_newlines_only(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_to_blocks_with_code_block(self):
        md = """
```python
def hello_world():
    print("Hello, world!")
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```python\ndef hello_world():\n    print(\"Hello, world!\")\n```"])

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# H1\n\n## H2\n\n### H3"
        # Test that it creates h1, h2, h3 tags correctly

    def test_quote_block(self):
        md = "> This is a quote\n> with multiple lines"
        # Test blockquote creation

    def test_unordered_list(self):
        md = "* Item 1\n* Item 2\n* Item 3"
        # Test ul with li elements

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"  
        # Test ol with li elements

    def test_mixed_blocks(self):
        md = "# Title\n\nThis is a paragraph.\n\n* List item"
        # Test multiple different block types together



