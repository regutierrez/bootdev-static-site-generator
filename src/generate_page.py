from blocks import markdown_to_htmlnode


def extract_title(md: str) -> str:
    lines: list[str] = [line.strip() for line in md.split("\n")]
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No title found")


def generate_page(src: str, template_path: str, dst: str) -> None:
    print("generating page from ", src, "to", dst, "...")
    try:
        with open(src, "r") as file:
            md: str = file.read()
    except FileNotFoundError:
        raise Exception(f"{src} not found")

    title: str = extract_title(md)
    try:
        with open(template_path, "r") as file:
            template: str = file.read()
    except FileNotFoundError:
        raise Exception(f"{template_path} not found")

    converted_html: str = markdown_to_htmlnode(md).to_html()

    with open(dst, "w") as file:
        file.write(
            template.replace("{{ Title }}", title).replace(
                "{{ Content }}", converted_html
            )
        )
