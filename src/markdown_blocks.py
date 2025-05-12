from enum import Enum
import re
from htmlnode import HtmlNode
from text_node_functions import text_to_textnodes
from textnode import text_node_to_html_node
# Excellent progress! Your code is looking good. You've correctly implemented text_to_children and started handling the heading blocks.

# Now you need to implement the handling for all the other block types. Let's think about each one:

#     Paragraph - Create a <p> node with the block's content processed with text_to_children
#     Code Block - Create a <pre><code> structure, but don't process inline markdown
#     Quote - Create a <blockquote> node with processed content
#     Unordered List - Create a <ul> with <li> items for each line
#     Ordered List - Create a <ol> with <li> items for each line

# For code blocks, remember that you shouldn't use text_to_children - the assignment mentioned making a TextNode manually and using text_node_to_html_node.

# For lists (both ordered and unordered), you'll need to:

#     Split the block into lines
#     Remove the list markers (like "- " or "1. ")
#     Process each line with text_to_children
#     Create <li> nodes for each processed line
#     Add all <li> nodes as children to a parent <ul> or <ol> node

# Try adding these cases to your code. Where would you like to start?

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    PARAGRAPH = "paragraph"
    OLIST = "unordered_list"
    ULIST = "ordered_list"

def markdown_to_html_node(markdown):
    completed_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_match = re.match(r'^(#{1,6}) ', block)
            if heading_match:
                heading_level = len(heading_match.group(1))
                content = block[heading_match.end():]  # Get content after the match
                children = text_to_children(content)
                heading_node = HtmlNode(f"h{heading_level}", None, children, None)
                completed_nodes.append(heading_node)
        # Handle other block types...
    
    # Create a parent div node with all completed_nodes as children
    parent_node = HtmlNode("div", None, completed_nodes, None)
    return parent_node

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes
        

def markdown_to_blocks(markdown):
    final_blocks = []
    split_markdown = markdown.split("\n\n")
    for block in split_markdown:
        block = block.strip()
        if not block:
            continue
        else:
            final_blocks.append(block)
             
    return final_blocks


def block_to_block_type(block):
    lines = block.split('\n')
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH
    # if re.match(r'^#{1,6} ', block):
    #     return BlockType.HEADING
    
    # if _is_ordered_list(lines):
    #     return BlockType.ORDERED_LIST

    

# def _is_ordered_list(lines):
#     if not lines:
#         return False
    
#     for i, line in enumerate(lines):
#         # Check if the line starts with the correct number (i+1)
#         expected = f"{i+1}. "
#         if not line.startswith(expected):
#             return False
    # return True