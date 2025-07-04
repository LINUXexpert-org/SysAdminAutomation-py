#!/usr/bin/env python3
"""
disk_cleanup.py - Disk Usage & Cleanup: Report disk usage and identify large files; optionally free space.

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
    disk_cleanup.py [--clean]

Description:
    Without --clean, displays disk usage and the top 10 largest files on the system.
    With --clean (requires root), cleans package caches and deletes old temporary files (older than 7 days).
"""
import sys
import os
import shutil
import time
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def show_disk_usage_and_large_files():
    """Print disk usage overview and top 10 largest files."""
    logging.info("==== Disk Usage Overview ====")
    # Use 'df -h' to get disk usage (excluding tmpfs/devtmpfs) for accuracy
    try:
        df_output = subprocess.check_output(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], text=True)
    except Exception as e:
        logging.error(f"Unable to retrieve disk usage (df failed): {e}")
        df_output = ""
    if df_output:
        # Log the df output as a single multi-line string
        logging.info("\n" + df_output.strip())
    logging.info("\n==== Top 10 Largest Files ====")
    # Find top 10 largest files in the filesystem
    largest_files = []
    # Skip certain virtual or system paths to avoid delays or permission issues
    skip_dirs = {"/proc", "/run", "/sys", "/dev"}
    for root, dirs, files in os.walk("/", topdown=True):
        # Optionally skip crossing into other filesystems or special dirs
        if root in skip_dirs:
            dirs[:] = []  # don't recurse into these
            continue
        for name in files:
            file_path = os.path.join(root, name)
            try:
                size = os.path.getsize(file_path)
            except Exception:
                continue
            largest_files.append((size, file_path))
    # Get top 10 by size
    largest_files.sort(reverse=True, key=lambda x: x[0])
    for size, path in largest_files[:10]:
        size_mb = size / (1024*1024)
        logging.info(f"{size_mb:.1f} MB - {path}")
    logging.info("\n(To actually free space, run: %s --clean)" % sys.argv[0])

def clean_package_caches_and_temp():
    """Perform cleanup of package caches and temporary files (requires root)."""
    # Ensure running as root
    if os.name != 'nt':  # only check on POSIX
        if os.geteuid() != 0:
            logging.error("Run as root to perform cleanup.")
            sys.exit(1)
    logging.info("Cleaning package caches and temporary files...")
    # Package manager cache cleanup
    try:
        if shutil.which("apt-get"):
            subprocess.run(["apt-get", "clean"], check=True)
        elif shutil.which("dnf"):
            subprocess.run(["dnf", "clean", "all"], check=True)
        elif shutil.which("yum"):
            subprocess.run(["yum", "clean", "all"], check=True)
        elif shutil.which("pacman"):
            subprocess.run(["pacman", "-Scc", "--noconfirm"], check=True)
        # (If other package managers like zypper, add similarly if needed)
    except subprocess.CalledProcessError as e:
        logging.warning(f"Package cache clean command failed: {e}")
    # Clean /tmp and /var/tmp files older than 7 days
    now = time.time()
    cutoff = now - 7*24*3600
    for tmpdir in ["/tmp", "/var/tmp"]:
        if os.path.isdir(tmpdir):
            # Remove files older than 7 days
            for root, dirs, files in os.walk(tmpdir, topdown=False):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    try:
                        if os.path.getmtime(fpath) < cutoff:
                            os.remove(fpath)
                    except Exception:
                        continue
                # Remove empty directories older than 7 days
                for dname in dirs:
                    dpath = os.path.join(root, dname)
                    try:
                        if not os.listdir(dpath) and os.path.getmtime(dpath) < cutoff:
                            os.rmdir(dpath)
                    except Exception:
                        continue
    logging.info("Temporary files older than 7 days removed from /tmp and /var/tmp.")
    logging.info("Disk cleanup completed.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments: just show disk usage info
        show_disk_usage_and_large_files()
        sys.exit(0)
    elif len(sys.argv) == 2 and sys.argv[1] == "--clean":
        clean_package_caches_and_temp()
    else:
        logging.error(f"Usage: {sys.argv[0]} [--clean]")
        sys.exit(1)
