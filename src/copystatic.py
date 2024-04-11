import os
import shutil

# WARNING: file paths here are relative, depending on where you executed the script
# if you executed it in the root folder (`python src/copystatic.py`), the root folder
# is your current folder


def copy_static(src: str = "static", dst: str = "public") -> None:
    if not os.path.exists(src):
        raise Exception(f"{src} not found")

    if not os.path.exists(dst) and os.path.isdir(src):
        print(f"path {dst} does not exist. creating folder...")
        os.mkdir(dst)
    if os.path.isfile(src):
        print("copying file", src, "to", dst)
        shutil.copy(src, dst)
        return

    for item in os.listdir(src):
        item_src_path: str = os.path.join(src, item)
        item_dst_path: str = os.path.join(dst, item)

        copy_static(item_src_path, item_dst_path)
