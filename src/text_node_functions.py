import re
from enum import Enum
from textnode import TextNode, TextType


def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    image_matches = re.findall(image_regex, text)
    return image_matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    link_matches = re.findall(link_regex, text)
    return link_matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: 
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception("Invalid Markdown Syntax, closing delimiter not found...")
            for i, part in enumerate(split_node):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, node.text_type))
                else:
                    new_nodes.append(TextNode(part, text_type))
               
    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        current_text = node.text
        if node.text == "":
            continue
        
        else:
            extracted_link = extract_markdown_images(current_text)
            
            if not extracted_link:
                new_nodes.append(node)
                continue
            
            while extracted_link:
                alt, url = extracted_link[0]
                pattern = f"![{alt}]({url})"
                sections = current_text.split(pattern, 1)
                text = sections[0]
                
                if sections[0]:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                    
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                current_text = sections[1]
                extracted_link = extract_markdown_images(current_text) 
                
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
                
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        current_text = node.text
        if node.text == "":
            continue
        
        else:
            extracted_link = extract_markdown_links(current_text)
            
            if not extracted_link:
                new_nodes.append(node)
                continue
            
            while extracted_link:
                  
                alt, url = extracted_link[0]
                pattern = f"[{alt}]({url})"
                sections = current_text.split(pattern, 1)
                text = sections[0]
                
                if sections[0]:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                    
                new_nodes.append(TextNode(alt, TextType.LINK, url))
                current_text = sections[1]
                extracted_link = extract_markdown_links(current_text) 
                
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
                
    return new_nodes


def text_to_textnodes(text):
    # Start with a list containing one text node with the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply each splitting function in sequence
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes



