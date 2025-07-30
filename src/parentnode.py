from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Tag cannot be None")
        if self.children == None:
            raise ValueError("Children cannot be None")
        return f"<{self.tag}{self.props_to_html()}>{self.iterate_children()}</{self.tag}>"
    
    def iterate_children(self):
        if not self.children:
            return ""
        return "".join([child.to_html() for child in self.children])
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""
        
        props_str = " ".join([f"{key}={value}" for key, value in self.props.items()])
        return f" {props_str}"
    
    def __repr__(self):
        print(f"{self.tag}, {self.value}, {self.children}, {self.props}")

    def __eq__(self, value):
        if self.tag != value.tag:
            return False
        if self.value != value.value:
            return False
        if self.children != value.children:
            return False
        if self.props != value.props:
            return False
        return True