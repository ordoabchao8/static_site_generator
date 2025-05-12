import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from text_node_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):
# ---- TEST MARKDOWN BLOCKS BLOCK TO BLOCK TYPE ---
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    

# ---- TEST MARKDOWN TO BLOCKS STANDALONE FUNCTION --
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_multiple_extra_new_lines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """

This is a paragraph.

This is another paragraph.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph.",
            ],
        )
        
    # ---- TESTS FOR STANDALONE FUNCTION SPLIT_NODES_LINK
    def test_split_images_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,)
        
    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)  # Should return original node

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)  # Should return original node

    def test_split_images_only_image(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")], new_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[link text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("link text", TextType.LINK, "https://example.com")], new_nodes)
   
    def test_split_links_multiple_nodes(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text",),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(split_nodes_link([node]), expected_nodes)
        
    def test_split_links_not_eq(self):
        node = TextNode("This is text with a link to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text",),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertNotEqual(split_nodes_link([node]), expected_nodes)
        
            
    
    
    # ---- Test TEXT NODE STANDALONE FUNCTION FOR EXTRACTING MARKDOWN FROM NODES---
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    
    # ---- Test TEXT NODE STANDALONE FUNCTION FOR CONVERTING MARKDOWN TO TEXTNODES
    def test_text_node_standalone_function_invalid_markdown_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_text_node_standalone_function_multiple_invalid_markdown_delimiters(self):
        node = TextNode("This is text with a `code block and another` `code block  word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_text_node_standalone_function_test_text_type_vs_other_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(node2, expected_nodes)
       
    def test_text_node_standalone_function_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        node2 = split_nodes_delimiter([node], "**", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(node2, expected_nodes)
    
    def test_text_node_standalone_function_italic_delimiter(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        node2 = split_nodes_delimiter([node], "_", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(node2, expected_nodes)
    
    def test_text_node_standalone_function_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(node2, expected_nodes)
    
    def test_text_node_standalone_function_empty_code_span(self):
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