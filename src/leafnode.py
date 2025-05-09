from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        if props_html:
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        else: 
            return f"<{self.tag}>{self.value}</{self.tag}>"
            
    
    def __eq__(self, other_node):
        if (self.tag == other_node.tag and 
            self.value == other_node.value and 
            self.props == other_node.props):
            return True
        return False
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.props})"
    
    