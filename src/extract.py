import re
from block import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.paragraph:
            # Normalize whitespace: replace newlines and multiple spaces with single spaces
            normalized_text = ' '.join(block.split())
            child_nodes = text_to_children(normalized_text)
            paragraph_node = ParentNode(tag="p", children=child_nodes)
            node_list.append(paragraph_node)

        if block_type == BlockType.heading:
            count = 0
            for char in block:
                if char == '#':
                    count += 1
                else:
                    break  # Stop when you hit the first non-# character
            heading_text = block[count:].strip()
            child_nodes = text_to_children(heading_text)
            heading_node = ParentNode(tag=f"h{count}", children=child_nodes)
            node_list.append(heading_node)

        if block_type == BlockType.code:
            # First, extract the code content
            lines = block.split('\n')
            inner_lines = lines[1:-1]  # Skip first and last line
            stripped_lines = [line.lstrip() for line in inner_lines]
            code_content = '\n'.join(stripped_lines)
            if inner_lines:  # If there was content, add final newline
                code_content += '\n'
            
            # Then create the inner <code> node with the cleaned content
            code_node = LeafNode(tag="code", value=code_content)
            # Create the outer <pre> node with code_node as its child
            pre_node = ParentNode(tag="pre", children=[code_node])
            node_list.append(pre_node)

        if block_type == BlockType.quote:
            lines = block.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove the "> " prefix from each line
                if line.startswith("> "):
                    cleaned_lines.append(line[2:])  # Remove first 2 characters ("> ")
                elif line.startswith(">"):
                    cleaned_lines.append(line[1:])  # Remove just the ">"
                else:
                    cleaned_lines.append(line)
            
            quote_text = '\n'.join(cleaned_lines)
            child_nodes = text_to_children(quote_text)
            quote_node = ParentNode(tag="blockquote", children=child_nodes)
            node_list.append(quote_node)

        if block_type == BlockType.unordered_list:
            lines = block.split('\n')
            li_nodes = []  # List to hold the <li> HTMLNodes
            
            for line in lines:
                line = line.strip()
                if line:
                    # Handle both "- " and "* " list markers
                    if line.startswith("- "):
                        item_text = line[2:]  # Remove "- "
                    elif line.startswith("* "):
                        item_text = line[2:]  # Remove "* "
                    else:
                        continue  # Skip lines that don't start with list markers
                    
                    # Create an <li> HTMLNode for this item
                    child_nodes = text_to_children(item_text)
                    li_node = ParentNode(tag="li", children=child_nodes)
                    li_nodes.append(li_node)
            
            # Create the <ul> node with all the <li> nodes as children
            ul_node = ParentNode(tag="ul", children=li_nodes)
            node_list.append(ul_node)

        if block_type == BlockType.ordered_list:
            lines = block.split('\n')
            li_nodes = []  # List to hold the <li> HTMLNodes
            
            for line in lines:
                line = line.strip()
                if line and ". " in line:
                    # Find the first ". " and split there
                    dot_index = line.find(". ")
                    if dot_index > 0:  # Make sure there's a number before the dot
                        item_text = line[dot_index + 2:]  # Remove everything up to and including ". "
                        # Create an <li> HTMLNode for this item
                        child_nodes = text_to_children(item_text)
                        li_node = ParentNode(tag="li", children=child_nodes)
                        li_nodes.append(li_node)
            
            # Create the <ol> node with all the <li> nodes as children
            ol_node = ParentNode(tag="ol", children=li_nodes)
            node_list.append(ol_node)

    return ParentNode(tag="div", children=node_list)

def text_to_children(text):
    # Convert text to TextNodes (handles inline markdown)
    text_nodes = text_to_textnodes(text)
    # Convert TextNodes to HTMLNodes
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # You need this function
        html_nodes.append(html_node)
    return html_nodes

