from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# class BlockNode:
#     def __init__(self, text: str, block_type: BlockType, url: str = None):
#         self.text = text
#         self.block_type = block_type
#         self.url = url

#     def __eq__(self, value) -> bool:
#         if self.text != value.text:
#             return False
#         if self.block_type != value.block_type:
#             return False
#         if self.url != value.url:
#             return False
#         return True
        
#     def __repr__(self):
#         return f"TextNode({self.text}, {self.text_type.value}, {self.url})"