import re
from textnode import TextType
from textnode import TextNode
from utils import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes =[]

    for nodes in old_nodes:
        if nodes.text_type == TextType.TEXT:
            if delimiter in nodes.text:
                split_parts = nodes.text.split(delimiter)
                if len(split_parts) % 2 == 0:
                    # Instead of raising Exception:
                    new_nodes.append(nodes)  # Just keep the node unchanged
                    continue  # Move to next node
                for index, value in enumerate(split_parts):
                    if value == "":
                        continue  # Skip empty segments
                    if index % 2 == 0:
                        new_node = TextNode(value, TextType.TEXT)
                        new_nodes.append(new_node)
                    else:
                        new_node = TextNode(value, text_type)
                        new_nodes.append(new_node)
            else:
                new_nodes.append(nodes)  # No delimiter, keep as is
                    
        else:
            new_nodes.append(nodes)

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current_text = node.text

            # Extract images from the text of this node
            images = extract_markdown_images(node.text)
            # Now, use the 'images' list to help split the node.text
            # ... your splitting logic here ...
            for alt_text, url in images:
                current_text.find(f"![{alt_text}]({url})")
                # Find the index of the image in the current text
                my_string = current_text.find(f"![{alt_text}]({url})")
                image_index = my_string if my_string != -1 else 0

                if current_text.find(f"![{alt_text}]({url})") == -1:
                    # If the image is not found in the current text, continue to the next image
                    continue

                text_before_image = current_text[:image_index]

                text_after_image = current_text[image_index + len(f"![{alt_text}]({url})"):]


                # If the text before the image is not empty, create a text node for it
                if text_before_image != "":
                    new_nodes.append(TextNode(text_before_image, TextType.TEXT))
                # Create the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                # Update the current text to be the text after the image
                current_text = text_after_image

            if current_text == "":
                # If there's no remaining text after processing images, skip adding a new node
                continue
            # If there's remaining text after processing images, add it as a text node
            new_nodes.append(TextNode(current_text, TextType.TEXT))

        else:
            # If it's not a text node, just add it to new_nodes
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            current_text = node.text

            # Extract images from the text of this node
            links = extract_markdown_links(node.text)

            # Now, use the 'images' list to help split the node.text
            # ... your splitting logic here ...
            for alt_text, url in links:
                current_text.find(f"![{alt_text}]({url})")
                # Find the index of the image in the current text
                my_string = current_text.find(f"[{alt_text}]({url})")
                links_index = my_string if my_string != -1 else 0

                if current_text.find(f"[{alt_text}]({url})") == -1:
                    # If the image is not found in the current text, continue to the next image
                    continue

                text_before_links = current_text[:links_index]

                text_after_links = current_text[links_index + len(f"[{alt_text}]({url})"):]


                # If the text before the image is not empty, create a text node for it
                if text_before_links != "":
                    new_nodes.append(TextNode(text_before_links, TextType.TEXT))
                # Create the image node
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))

                # Update the current text to be the text after the image
                current_text = text_after_links

            if current_text == "":
                # If there's no remaining text after processing images, skip adding a new node
                continue
            # If there's remaining text after processing images, add it as a text node
            new_nodes.append(TextNode(current_text, TextType.TEXT))

        else:
            # If it's not a text node, just add it to new_nodes
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	return nodes	

