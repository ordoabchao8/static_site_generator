import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    
    # TEST PROPS
    def test_parent_node_props_to_html(self):
        child_node = LeafNode("p", "child")
        parent_node = ParentNode("a", [child_node], {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(parent_node.to_html(), '<a href="https://www.boot.dev" target="_blank"><p>child</p></a>')
                    
    # TEST TAG
    def test_parent_node_with_none_tag_raises_value_error(self):
        child_node = LeafNode("p", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    # TEST CHILDREN
    def test_parent_children_eq_none_raises_err(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_parent_children_empty_list_raises_err(self):
        parent_node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("p", "first child")
        child2 = LeafNode("span", "second child")
        child3 = LeafNode("b", "third child")          
        parent_node = ParentNode("span", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), "<span><p>first child</p><span>second child</span><b>third child</b></span>")  
        
    def test_parent_to_html_mixed_children(self):
        child1 = LeafNode("p", "first child")
        child2 = LeafNode("span", "second child")      
        parent_node = ParentNode("span", [child1, child2])
        child4 = LeafNode("a", "fourth child inside main parent")
        main_parent_node = ParentNode("p", [parent_node, child4])
        self.assertEqual(main_parent_node.to_html(), "<p><span><p>first child</p><span>second child</span></span><a>fourth child inside main parent</a></p>")
        

if __name__ == "__main__":
    unittest.main()