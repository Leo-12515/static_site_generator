import os
import shutil
from extract import markdown_to_html_node  # Assuming this is a custom module for converting markdown to HTML
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

src_dir = "static"
dst_dir = "docs"

if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)
os.mkdir(dst_dir)

def copy_recursive(src_dir, dst_dir):

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)  # Full path in "static"
        dst_path = os.path.join(dst_dir, item)  # Full path in "public"
        
        
        if os.path.isfile(src_path):
            # This copies the file from static to public:
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            # Create the destination directory if it doesn't exist
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copy_recursive(src_path, dst_path)

copy_recursive(src_dir, dst_dir)

def extract_title(markdown):
    """
    Extracts the title from the first line of a markdown file.
    """
    if not markdown:
        raise Exception("Markdown does not start with a title line.")
    first_line = markdown.split('\n')[0]
    if first_line.startswith('# '):
        return first_line.lstrip('# ').strip()
    raise Exception("Markdown does not start with a title line.")

def generate_page(from_path, template_path, dest_path, base_path):
    # 1. Read markdown file
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    # 2. Read template file
    with open(template_path, 'r') as f:
        template = f.read()
    
    # 3. Extract title
    title = extract_title(markdown)
    
    # 4. Convert markdown to HTML node, then to HTML string
    content_node = markdown_to_html_node(markdown)
    content_html = content_node.to_html()
    
    # 5. Replace placeholders in template
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page_content = page_content.replace('href="/', f'href="{base_path}')
    page_content = page_content.replace('src="/', f'src="{base_path}')
    
    # 6. Get the directory for the destination file
    dest_dir_path = os.path.dirname(dest_path)
    
    # 7. Create the destination directory if it doesn't exist
    os.makedirs(dest_dir_path, exist_ok=True) 
    
    # 8. Write the full HTML page to the destination path
    with open(dest_path, 'w') as f:
        f.write(page_content)
    
    # 9. Print the completion message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    """
    Recursively generates HTML pages from markdown files in a directory.
    """
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith('.md'):
            # Generate page for markdown file
            dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
            generate_page(item_path, template_path, dest_path, base_path)
        elif os.path.isdir(item_path):
            # Create corresponding directory in destination
            new_dest_dir = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir, exist_ok=True)
            # Recur into the subdirectory
            generate_pages_recursive(item_path, template_path, new_dest_dir, base_path)


generate_pages_recursive(
    dir_path_content="content/",
    template_path="template.html",
    dest_dir_path="docs/",
    base_path=basepath
)


"""from textnode import TextNode, TextType

def main():
    # Create a TextNode with dummy values
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # Print the node
    print(node)


if __name__ == "__main__":
    main()
"""