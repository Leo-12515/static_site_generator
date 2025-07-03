import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
        
        
class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with empty props (None or {})
        node1 = HTMLNode(props=None)
        self.assertEqual(node1.props_to_html(), "")
        
        node2 = HTMLNode(props={})
        self.assertEqual(node2.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
        
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        # Note: The order of attributes might vary, so we need to check for both possibilities
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Wizard bear lives here.")
        self.assertEqual(node.to_html(), "<span>Wizard bear lives here.</span>")
        
    def test_leaf_to_html_tag(self):
        node = LeafNode(None, "plain text only")
        self.assertEqual(node.to_html(), "plain text only")
        
    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>'
        )

    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "test")]).to_html()
    
    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()