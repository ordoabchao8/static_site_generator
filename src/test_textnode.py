import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from text_node_functions import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    # ---- Test TEXT NODE STANDALONE FUNCTION FOR CONVERTING MARKDOWN TO TEXTNODES
    def test_text_node_standalone_function_invalid_markdown_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_text_node_standalone_function_multiple_invalid_markdown_delimiters(self):
        node = TextNode("This is text with a `code block and another` `code block  word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_text_node_empty_code_span(self):
        node = TextNode("This is text with a `` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        # Check there’s an empty code node in the right place
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    #---- Test TEXT NODE TO HTML NODE USING standalone function
    def test_text_node_to_html_node_type_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_node_to_html_node_type_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_text_node_to_html_node_type_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")
        
    def test_text_node_to_html_node_type_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        
    def test_text_node_to_html_node_type_link(self):
        node = TextNode("This is a link text node", TextType.LINK, {"href": "https://www.boot.dev"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": html_node.props["href"]})
        
    def test_text_node_to_html_node_type_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, {"src": "https://example.com/image.png"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text for image")
    
    #---- Test equal to exactly ------------------------------
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    #-------------------------------------------------------
    
    #---- Test TEXT TYPE -------------------------------------
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node.text_type.value, node2.text_type.value)
        
    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type.value, node2.text_type.value)
    #-----------------------------------------------------------------   
     
    #---- Test URL ------------------------------
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.props)
        
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)
    #-------------------------------------------------------------------
    
    #---- TEST TEXT-----------------------
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node.text, node2.text)
        
    #--------- TEST REPR------------------------------
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
     #-----------------------------------------------------------   
        
if __name__ == "__main__":
    unittest.main()