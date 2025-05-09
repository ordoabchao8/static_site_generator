from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # first_delimiter = node.text.find(delimiter)
            # second_delimiter = node.text[first_delimiter:].find(delimiter)
            # if second_delimiter == -1:
            #  
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception("Invalid Markdown Syntax, closing delimiter not found...")
            for i, part in enumerate(split_node):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, node.text_type))
                else:
                    new_nodes.append(TextNode(part, text_type))
               
    return new_nodes
    
    

