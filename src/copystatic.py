import os
import shutil


def copy_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.makedirs(destination)
	
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        if os.path.isdir(src_path):
            print(f"Copying directory: {src_path} to {dst_path}")
            copy_contents(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
            print(f"Copying file: {src_path} to {dst_path}")




