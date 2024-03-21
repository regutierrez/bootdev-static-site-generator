class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None) -> None:
        self.text: str  = text
        self.text_type: str = text_type
        self.url: str | None = url

    def eq(self, TextNode) -> bool:
        if self == TextNode:
            return True
        return False

    def repr(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
