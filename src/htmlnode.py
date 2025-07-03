class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        attributes = [f'{k}="{v}"' for k, v in self.props.items()]

        if not attributes:
            return ""
        return " " + ' '.join(attributes)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value

        attributes = [f'{k}="{v}"' for k, v in (self.props or {}).items()]
        attrs_str = " " + ' '.join(attributes) if attributes else ""

        return f"<{self.tag}{attrs_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag must be provided for ParentNode")

        if self.children == None:
            raise ValueError("ParentNode must have at least one child")

        attributes = [f'{k}="{v}"' for k, v in (self.props or {}).items()]
        attrs_str = " " + ' '.join(attributes) if attributes else ""

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attrs_str}>{children_html}</{self.tag}>"
