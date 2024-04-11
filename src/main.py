from copystatic import copy_static
import os
import shutil

if __name__ == "__main__":
    public_folder: str = "public"
    if os.path.exists(public_folder):
        print(f"removing {public_folder} folder...")
        shutil.rmtree(public_folder)

    print("copying static files to public directory...")
    copy_static()
