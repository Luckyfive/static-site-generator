from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
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