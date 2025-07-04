#!/usr/bin/env python3
"""
log_rotate.py - Log Rotation: Compress and remove old log files.

Usage:
    log_rotate.py [days]

Argument:
    days: Rotate (compress) logs older than this many days (default is 7 days).

Description:
    Compresses uncompressed .log files older than N days in /var/log, 
    and deletes .gz log archives older than 90 days.
"""
import sys
import os
import gzip
import shutil
import time
import logging
from stat import filemode

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def rotate_logs(days: int):
    """Compress .log files older than `days` days and remove .gz archives older than 90 days."""
    # Ensure running as root for system log rotation
    if os.name != 'nt':  # only check on POSIX systems
        try:
            if os.geteuid() != 0:
                logging.error("Please run as root to rotate system logs.")
                sys.exit(1)
        except AttributeError:
            # os.geteuid may not exist on some platforms (e.g. Windows); skip if so.
            pass
    cutoff = time.time() - days*24*3600
    logging.info(f"Rotating logs older than {days} days...")
    # Compress uncompressed .log files older than cutoff
    compressed_count = 0
    for root, dirs, files in os.walk("/var/log"):
        for fname in files:
            if not fname.endswith(".log"):
                continue
            fpath = os.path.join(root, fname)
            try:
                st = os.stat(fpath)
            except FileNotFoundError:
                continue
            if st.st_mtime < cutoff and not fpath.endswith(".gz"):
                gz_path = fpath + ".gz"
                try:
                    with open(fpath, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                except Exception as e:
                    logging.warning(f"Failed to compress {fpath}: {e}")
                    continue
                # If compression succeeded, remove the original .log file
                try:
                    os.remove(fpath)
                    compressed_count += 1
                except Exception as e:
                    logging.warning(f"Failed to remove original log {fpath}: {e}")
    if compressed_count:
        logging.info(f"Compressed logs older than {days} days.")
    # Remove compressed log archives older than 90 days
    cutoff90 = time.time() - 90*24*3600
    removed_count = 0
    for root, dirs, files in os.walk("/var/log"):
        for fname in files:
            if fname.endswith(".gz"):
                fpath = os.path.join(root, fname)
                try:
                    st = os.stat(fpath)
                except FileNotFoundError:
                    continue
                if st.st_mtime < cutoff90:
                    try:
                        os.remove(fpath)
                        removed_count += 1
                    except Exception as e:
                        logging.warning(f"Failed to remove old archive {fpath}: {e}")
    if removed_count:
        logging.info("Removed log archives older than 90 days.")

if __name__ == "__main__":
    # Determine days argument (default 7 if not a positive integer)
    days = 7
    if len(sys.argv) >= 2:
        try:
            # Only accept positive integer values for days
            val = int(sys.argv[1])
            if val >= 0:
                days = val
        except ValueError:
            # Non-integer argument is ignored, default to 7
            days = 7
    rotate_logs(days)
