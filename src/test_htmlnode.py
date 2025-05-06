import unittest

from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode("<p>", "hello!", {"href": "https://boot.dev", "target": "_blank"})
        node2 = HtmlNode("<p>", "hello!", {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = HtmlNode("<p>", "hello!", {"href": "https://boot.dev", "target": "_blank"})
        node2 = HtmlNode("<>", "hello!", {"href": "https://boot.dev", "target": "_blank"})
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = HtmlNode("<p>", "hello!", None, {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            f"HtmlNode(<p>, hello!, None, {{'href': 'https://boot.dev', 'target': '_blank'}})", repr(node)
        )