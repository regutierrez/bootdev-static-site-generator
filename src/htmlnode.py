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
        props_html: str = ""

        if self.props == None:
            return ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'

        return props_html

    def __repr__(self) -> str:
        return f"tag = {self.tag}\nvalue = {self.value}\nchildren = {self.children}\nprops = {self.props_to_html()}"


test = HTMLNode("a", "testing lang", props={"href": "gl.com", "target": "_blank"})

print(test)
