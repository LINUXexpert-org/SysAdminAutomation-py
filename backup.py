#!/usr/bin/env python3
"""
backup.py - Backup Utility: Archive directories into compressed tarballs for backups.

Copyright (C) 2025 LINUXexpert.org

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
for more details.

You should have received a copy of the GNU General Public License along 
with this program. If not, see <https://www.gnu.org/licenses/>.

Usage:
    backup.py <source_directory> <destination_directory>

Description:
    Creates a .tar.gz archive of the source directory inside the destination directory.
"""
import sys
import os
import tarfile
import logging
from datetime import datetime

# Configure logging to console with time and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_backup(source_dir: str, dest_dir: str) -> None:
    """Create a compressed tarball of source_dir inside dest_dir."""
    # Ensure source directory exists
    if not os.path.isdir(source_dir):
        logging.error(f"Source directory '{source_dir}' not found!")
        raise FileNotFoundError(f"Source directory '{source_dir}' not found")
    # Ensure destination directory exists (create if needed)
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create destination directory '{dest_dir}': {e}")
        raise

    # Construct archive name with date stamp
    base_name = os.path.basename(os.path.abspath(source_dir.rstrip('/')))
    date_str = datetime.now().strftime("%Y%m%d")
    archive_name = f"{base_name}-backup-{date_str}.tar.gz"
    archive_path = os.path.join(dest_dir, archive_name)

    # Create tar.gz archive
    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            # Add the source directory contents (at top-level inside archive)
            tar.add(source_dir, arcname=base_name)
        logging.info(f"Backup successful: {archive_path}")
    except Exception as e:
        # Remove incomplete archive file if created
        if os.path.exists(archive_path):
            os.remove(archive_path)
        logging.error(f"Backup failed for {source_dir}: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error(f"Usage: {sys.argv[0]} <source_directory> <destination_directory>")
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    try:
        create_backup(src, dest)
    except Exception:
        sys.exit(1)
