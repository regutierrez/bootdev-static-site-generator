from copystatic import copy_static
from generate_page import generate_pages_recursively
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if os.path.exists(dir_path_public):
        print("deleting public folder...")
        shutil.rmtree(dir_path_public)

    print("copying static files to public directory...")
    copy_static(dir_path_static, dir_path_public)

    generate_pages_recursively(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
