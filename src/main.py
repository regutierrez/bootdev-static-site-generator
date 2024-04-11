from copystatic import copy_static
import os
import shutil

if __name__ == "__main__":
    public_folder: str = "public"
    if os.path.exists(public_folder):
        shutil.rmtree(public_folder)

    copy_static()
