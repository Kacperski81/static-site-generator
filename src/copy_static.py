"""
Utility to recursively copy files and directories from a source to destination.
"""

import os
import shutil


def copy_dir(src, dst):
    """
    Recursively copy all contents from src directory to dst directory.
    Deletes all existing contents in the destination directory first.
    
    Args:
        src: Source directory path
        dst: Destination directory path
        
    Logs each file copied to stdout for debugging.
    """
    # Delete destination directory if it exists
    if os.path.exists(dst):
        print(f"Removing existing destination directory: {dst}")
        shutil.rmtree(dst)
    
    # Create the destination directory
    print(f"Creating destination directory: {dst}")
    os.mkdir(dst)
    
    # Recursively copy contents
    _copy_dir_recursive(src, dst)


def _copy_dir_recursive(src, dst):
    """
    Helper function for recursive copying.
    
    Args:
        src: Source directory path
        dst: Destination directory path
    """
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory, create it and recurse
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_dir_recursive(src_path, dst_path)
