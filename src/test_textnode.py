import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me", TextType.LINK, "https://examp.com")
        self.assertNotEqual(node, node2)

    def test_url_emp(self):
        node = TextNode("Click me", TextType.LINK, "")
        node2 = TextNode("Click me", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is BOLD text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is BOLD text")
    
    def test_italic(self):
        node = TextNode("This is Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is Italic text")

    def test_code(self):
        node = TextNode("This is Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is Code text")

    def test_link(self):
        node = TextNode("This is link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href" : "https://example.com"})
        self.assertEqual(html_node.value, "This is link text")

    def test_image(self):
        node = TextNode("A bear avatar", TextType.IMAGE, "https://bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src" : "https://bear.png", "alt": "A bear avatar"})
        self.assertEqual(html_node.value, "")


if __name__ == "__main__":
    unittest.main()
