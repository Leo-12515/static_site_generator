import re
from enum import Enum, auto

class BlockType(Enum):
    paragraph = auto()
    heading = auto()
    code = auto()
    quote = auto()
    unordered_list = auto()
    ordered_list = auto()

def block_to_block_type(block):
    """
    Converts a block of text to its corresponding BlockType.
    
    Args:
        block (str): The block of text to convert.
        
    Returns:
        BlockType: The type of the block.
    """
    lines = block.splitlines()

    if not lines or all(not line.strip() for line in lines):
        return BlockType.paragraph
    
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break  # not an ordered list!
    else:
        return BlockType.ordered_list  # all lines passed

    if all(line.startswith(">") for line in lines):
        return BlockType.quote
    if all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    if re.match(r'^#{1,6} ', lines[0]):
        return BlockType.heading
    if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.code
    return BlockType.paragraph

