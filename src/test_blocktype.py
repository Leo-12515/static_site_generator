import pytest
from block import BlockType, block_to_block_type

def test_block_to_block_type():
    # Test paragraph block
    assert block_to_block_type("This is a simple paragraph.") == BlockType.paragraph

    # Test heading block
    assert block_to_block_type("# This is a heading") == BlockType.heading
    assert block_to_block_type("## This is a subheading") == BlockType.heading

    # Test code block
    assert block_to_block_type("```\nprint('Hello, World!')\n```") == BlockType.code

    # Test quote block
    assert block_to_block_type("> This is a quote\n> with multiple lines") == BlockType.quote

    # Test unordered list block
    assert block_to_block_type("- Item 1\n- Item 2\n- Item 3") == BlockType.unordered_list

    # Test ordered list block
    assert block_to_block_type("1. First item\n2. Second item\n3. Third item") == BlockType.ordered_list

    # Test mixed content (should default to paragraph)
    assert block_to_block_type("This is a paragraph.\n- List item") == BlockType.paragraph

    # Test bad heading with 7 hashes
    assert block_to_block_type("####### This is a wrong heading with 7 hashes") == BlockType.paragraph

    #Test ordered list with out of order numbers(should default to paragraph)
    assert block_to_block_type("1. First item\n3. Third item\n2. Second item") == BlockType.paragraph

    # Test unordered list with missing dashes
    assert block_to_block_type("Item 1\nItem 2\nItem 3") == BlockType.paragraph

    # Test unordered list with a single missing dash
    assert block_to_block_type("- Item 1\nItem 2\n- Item 3") == BlockType.paragraph

    # Test Code block with only three backticks and no content
    assert block_to_block_type("```\n```") == BlockType.code

    # Test for Quote where one line doesn't start with '>'
    assert block_to_block_type("> This is a quote\nThis is not a quote") == BlockType.paragraph
    
    # Test for Quote with no '>' at all
    assert block_to_block_type("This is not a quote") == BlockType.paragraph

    # Test for empty string
    assert block_to_block_type("") == BlockType.paragraph


