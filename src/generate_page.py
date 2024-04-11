def extract_title(md: str) -> str:
    lines: list[str] = [line.strip() for line in md.split("\n")]
    for line in lines:
        if line.startswith("# "):
            return line
    raise Exception("No title found")


def generate_page(src: str, template_path: str, dst: str) -> None:
    pass


extract_title("Hala kaaaa\n # testing\n  ## testing 2\n  # testing 3\n hahahaha")
