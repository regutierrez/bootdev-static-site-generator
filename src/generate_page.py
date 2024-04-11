from blocks import markdown_to_htmlnode
import os
from pathlib import Path


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


def generate_pages_recursively(src: str, template_path: str, dst: str) -> None:
    if not os.path.exists(src):
        raise Exception("source folder not found")

    # list all .md file paths in the src directory. str(path) because path returns a Path object
    src_subdir: list[str] = [str(path) for path in list(Path(src).glob("**/*.md"))]

    for md in src_subdir:
        new_dst_dir: str = os.path.join(dst, md.lstrip("content/").rstrip("index.md"))
        if not os.path.isdir(new_dst_dir):
            os.mkdir(new_dst_dir)
        print(f"converting {md} to {new_dst_dir}")
        generate_page(md, template_path, os.path.join(new_dst_dir, "index.html"))
