from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        string = ""
        if self.tag is None:
            raise ValueError("HTML tag is required for parent node")
        if self.children is None or not self.children:
            raise ValueError("Parent node must have children")
        
        for node in self.children:
            string += node.to_html()
            
        
        return f"<{self.tag}{self.props_to_html()}>{string}</{self.tag}>"
         
            
        

        