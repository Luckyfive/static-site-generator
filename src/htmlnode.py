class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError
    
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