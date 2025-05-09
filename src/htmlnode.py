class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props
    
    def __eq__(self, other_node):
        if (self.tag == other_node.tag and 
            self.value == other_node.value and 
            self.children == other_node.children and 
            self.props == other_node.props):
            return True
        return False
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"