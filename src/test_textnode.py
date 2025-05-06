import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
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
        self.assertIsNone(node.url)
        
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