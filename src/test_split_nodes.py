# test_split_nodes.py
import pytest
from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

def test_split_basic_code():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    assert new_nodes[0].text == "This is text with a "
    assert new_nodes[0].text_type == TextType.TEXT
    assert new_nodes[1].text == 'code block'
    assert new_nodes[1].text_type == TextType.CODE
    assert new_nodes[2].text == ' word'
    assert new_nodes[2].text_type == TextType.TEXT

def test_split_basic_bold():
    node = TextNode("This is text with a **code block** word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert new_nodes[0].text == "This is text with a "
    assert new_nodes[0].text_type == TextType.TEXT
    assert new_nodes[1].text == 'code block'
    assert new_nodes[1].text_type == TextType.BOLD
    assert new_nodes[2].text == ' word'
    assert new_nodes[2].text_type == TextType.TEXT

def test_basic_code_split():
    # Create input
    node = TextNode("Some text with `code` here", TextType.TEXT)
    
    # Call your function
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    
    # Check the results
    assert len(result) == 3  # Should have 3 nodes
    assert result[0].text == "Some text with "
    assert result[0].text_type == TextType.TEXT
    assert result[1].text == "code"
    assert result[1].text_type == TextType.CODE

    expected = [
    TextNode("Some text with ", TextType.TEXT),
    TextNode("code", TextType.CODE),
    TextNode(" here", TextType.TEXT)
    ]
    assert result == expected 


def test_split_basic_italic():
    node = TextNode("This is text with an _italic word_ here", TextType.TEXT)
    result = split_nodes_delimiter([node], "_", TextType.ITALIC)

    # Check the results
    assert len(result) == 3  # Should have 3 nodes
    assert result[0].text == "This is text with an "
    assert result[0].text_type == TextType.TEXT
    assert result[1].text == "italic word"
    assert result[1].text_type == TextType.ITALIC
    assert result[2].text == " here"
    assert result[2].text_type == TextType.TEXT

def test_split_no_delimiters():
    # Create a node with text that has no delimiters
    node = TextNode("This is text for no delimiters", TextType.TEXT)
    # Call split_nodes_delimiter 
    result = split_nodes_delimiter([node], "'", TextType.CODE)

    assert len(result) == 1  # Should have 1 node (the original)
    assert result[0].text == "This is text for no delimiters"
    assert result[0].text_type == TextType.TEXT

def test_split_multiple_delimiters():
    # Create a node with text that has 5 delimiters
    node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
    # Call split_nodes_delimiter 
    result = split_nodes_delimiter([node], "**", TextType.BOLD)

    assert len(result) == 5 
    assert result[0].text == "This has "
    assert result[0].text_type == TextType.TEXT
    assert result[1].text == "bold"
    assert result[1].text_type == TextType.BOLD
    assert result[2].text == " and "
    assert result[2].text_type == TextType.TEXT
    assert result[3].text == "more bold"
    assert result[3].text_type == TextType.BOLD
    assert result[4].text == " text"
    assert result[4].text_type == TextType.TEXT

def test_delimiter_without_closing():
    node = TextNode("This has **bold text without closing", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert nodes == [node]

def test_split_images():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])

    assert [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ] == new_nodes

def test_split_no_images():
    node = TextNode(
        "This is text with no images",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode("This is text with no images", TextType.TEXT)
        ] == new_nodes
    

def test_split_image_at_start():
    node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) is an image and here is another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" is an image and here is another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ] == new_nodes

def test_split_image_at_end():
    node = TextNode(
        "here is an image: ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode("here is an image: ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ] == new_nodes

def test_split_only_image():
    node = TextNode(
        "![image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode(
                "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ] == new_nodes

def test_split_image_error_syntax():
    node = TextNode(
        "![image(https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode(
                "![image(https://i.imgur.com/3elNhQu.png)", TextType.TEXT, 
            ),
        ] == new_nodes

def test_split_image_error_syntax2():
    node = TextNode(
        "[image(https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert[
            TextNode(
                "[image(https://i.imgur.com/3elNhQu.png)", TextType.TEXT, 
            ),
        ] == new_nodes

def test_split_back_to_back_images():
    node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    assert [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ] == new_nodes

def test_split_links():
    node = TextNode(
        "This is text with a link: [Link](https://www.google.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert [
            TextNode("This is text with a link: ", TextType.TEXT),
            TextNode("Link", TextType.LINK, "https://www.google.com"),
        ] == new_nodes

def test_split_several_links():
    node = TextNode(
        "This is text with a link: [Link](https://www.google.com) and another link: [Boot.dev](https://www.boot.dev) and another last link: [YouTube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert [
            TextNode("This is text with a link: ", TextType.TEXT),
            TextNode("Link", TextType.LINK, "https://www.google.com"),
            TextNode(" and another link: ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another last link: ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ] == new_nodes

def test_split_link_at_start():
    node = TextNode(
        "[Link](https://www.google.com) this is a link at the start",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert[
            TextNode("Link", TextType.LINK, "https://www.google.com"),
            TextNode(" this is a link at the start", TextType.TEXT),
        ] == new_nodes

def test_split_only_a_link():
    node = TextNode(
        "[Link](https://www.google.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert [
            TextNode("Link", TextType.LINK, "https://www.google.com"),
        ] == new_nodes

def test_split_link_syntax_error():
    node = TextNode(
        "[Link(https://www.google.com)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    assert [
            TextNode("[Link(https://www.google.com)", TextType.TEXT),
        ] == new_nodes
    
def test_bold_and_split_nodes_link_image():
    nodes = text_to_textnodes("This is **bold** text and [link](https://example.com) and ![image](https://example.com/image.png)")
    assert nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text and ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://example.com"),
        TextNode(" and ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
    ]

def test_plain_text():
    nodes = text_to_textnodes("Just a simple sentence.")
    assert nodes == [TextNode("Just a simple sentence.", TextType.TEXT)]

def test_italic():
    nodes = text_to_textnodes("This is _italic_ text.")
    assert nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text.", TextType.TEXT)
    ]

def test_code():
    nodes = text_to_textnodes("This is `code`.")
    assert nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(".", TextType.TEXT)
    ]

def test_mixed_styles():
    nodes = text_to_textnodes("Try **bold**, _italic_, and `code`!")
    assert nodes == [
        TextNode("Try ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(", ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(", and ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode("!", TextType.TEXT)
    ]

def test_link_with_bold_text():
    nodes = text_to_textnodes("[**bold link**](https://site.com)")
    assert nodes == [
        TextNode("**bold link**", TextType.LINK, "https://site.com"),
    ]

def test_image_with_italic_alt():
    nodes = text_to_textnodes("![alt _italic_](https://img.com/pic.png)")
    assert nodes == [
        TextNode("alt _italic_", TextType.IMAGE, "https://img.com/pic.png"),
    ]

def test_adjacent_markdown():
    nodes = text_to_textnodes("**bold**_italic_")
    assert nodes == [
        TextNode("bold", TextType.BOLD),
        TextNode("italic", TextType.ITALIC),
    ]

def test_empty_string():
    nodes = text_to_textnodes("")
    assert nodes == []

def test_only_delimiters():
    nodes = text_to_textnodes("****")
    assert nodes == []

def test_unclosed_bold():
    nodes = text_to_textnodes("This is **not closed bold")
    assert nodes == [TextNode("This is **not closed bold", TextType.TEXT)]

def test_unclosed_link():
    nodes = text_to_textnodes("[oops](url")
    assert nodes == [TextNode("[oops](url", TextType.TEXT)]

def test_back_to_back_styles():
    nodes = text_to_textnodes("**a**_b_`c`")
    assert nodes == [
        TextNode("a", TextType.BOLD),
        TextNode("b", TextType.ITALIC),
        TextNode("c", TextType.CODE)
    ]

def test_long_sentence_styles():
    text = "a _b_ c **d** e [f](x) g"
    nodes = text_to_textnodes(text)
    assert nodes == [
        TextNode("a ", TextType.TEXT),
        TextNode("b", TextType.ITALIC),
        TextNode(" c ", TextType.TEXT),
        TextNode("d", TextType.BOLD),
        TextNode(" e ", TextType.TEXT),
        TextNode("f", TextType.LINK, "x"),
        TextNode(" g", TextType.TEXT),
    ]



