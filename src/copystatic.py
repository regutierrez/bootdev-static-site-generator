import os
import shutil

# WARNING: file paths here are relative, depending on where you executed the script
# if you executed it in the root folder (`python src/copystatic.py`), the root folder
# is your current folder


def copy_static(src: str = "static", dst: str = "public") -> None:
    if not os.path.exists(src):
        raise Exception(f"{src} not found")

    if not os.path.exists(dst) or os.path.isfile(dst):
        print(f"path {dst} does not exist. creating folder...")
        os.mkdir(dst)
    if os.path.isfile(src):
        print("copying file", src, "to", dst)
        shutil.copy(src, dst)
        return

    items: list[str] = os.listdir(src)
    for item in items:
        print(f"in {item}")
        item_src_path: str = os.path.join(src, item)
        item_dst_path: str = os.path.join(dst, item)

        copy_static(item_src_path, item_dst_path)


copy_static()
