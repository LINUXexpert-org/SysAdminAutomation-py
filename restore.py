#!/usr/bin/env python3
"""
restore.py - Restore Utility: Restore files from backup archives.

Usage:
    restore.py <backup_archive.tar.gz> [target_directory]

Description:
    Extracts the given .tar.gz backup archive into the target directory (current directory if not specified).
"""
import sys
import os
import tarfile
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def restore_archive(archive_path: str, target_dir: str = ".") -> None:
    """Extract a tar.gz archive into the target directory."""
    if not os.path.isfile(archive_path):
        logging.error(f"Backup archive '{archive_path}' not found!")
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    # Use current directory if target_dir is not provided
    if target_dir == "":
        target_dir = "."
    # Ensure target directory exists
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create target directory '{target_dir}': {e}")
        raise

    # Extract the tar.gz archive
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=target_dir)
        logging.info(f"Restore successful to directory: {os.path.abspath(target_dir)}")
    except Exception as e:
        logging.error(f"Restore failed: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        logging.error(f"Usage: {sys.argv[0]} <archive.tar.gz> [target_directory]")
        sys.exit(1)
    archive = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) == 3 else "."
    try:
        restore_archive(archive, target)
    except Exception:
        sys.exit(1)
