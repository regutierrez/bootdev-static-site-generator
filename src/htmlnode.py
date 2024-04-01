class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list | None = children
        self.props: dict | None = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str | None:
        if self.props is None:
            return ""

        props_html: str = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'

        return props_html

    def __repr__(self) -> str:
        return f"HTMLNODE({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
    ) -> None:
        if value is None:
            raise ValueError

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value provided")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNODE({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list,
        props: dict | None = None,
    ) -> None:
        if children is None:
            raise ValueError
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag provided")
        if self.children is None:
            raise ValueError("No children provided")
        child_html: str = ""
        for child in self.children:
            child_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNODE({self.tag}, children: {self.children}, {self.props})"
