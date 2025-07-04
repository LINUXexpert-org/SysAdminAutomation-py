#!/usr/bin/env python3
"""
rsync_magic.py - Flexible rsync wrapper for safe synchronization and backups.

Usage:
    rsync_magic.py [--dry-run] <source> <destination>

Description:
    Synchronizes files from <source> to <destination> using rsync with a predefined set of safe options.
    The --dry-run option simulates the sync. Logs activity to /var/log/rsync_magic.log.
"""
import sys
import os
import subprocess
import logging
from datetime import datetime

# Configuration
LOG_FILE = "/var/log/rsync_magic.log"
EXCLUDE_FILE = "/etc/rsync_magic_excludes.txt"

# Set up logging to both console and log file
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(LOG_FILE, mode='a')])

if __name__ == "__main__":
    # Parse arguments
    dry_run = False
    args = sys.argv[1:]
    if len(args) == 0 or len(args) > 3:
        logging.error(f"Usage: {sys.argv[0]} [--dry-run] <source> <destination>")
        sys.exit(1)
    if args[0] == "--dry-run":
        dry_run = True
        args.pop(0)
    if len(args) != 2:
        logging.error(f"Usage: {sys.argv[0]} [--dry-run] <source> <destination>")
        sys.exit(1)
    source = args[0]
    dest = args[1]
    # Ensure source exists and is a directory
    if not os.path.isdir(source):
        logging.error(f"Error: Source directory '{source}' not found!")
        sys.exit(2)
    # Create destination directory if it doesn't exist
    os.makedirs(dest, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.info(f"Starting rsync at {timestamp}")
    # Build rsync options
    rsync_opts = [
        "-a",  # archive mode
        "-v",  # verbose
        "-z",  # compress
        "-h",  # human-readable numbers
        "-u",  # skip files newer on receiver
        "-P",  # progress and partial transfers
        "-c",  # checksum comparison
        "-x",  # don't cross filesystem boundaries
        "-A",  # preserve ACLs
        "-X",  # preserve extended attributes
        "--delete",  # delete extraneous files on dest
        "--numeric-ids",  # numeric uid/gid
        "--inplace",  # in-place updates
        "--backup",  # keep backups of changed/deleted files
        f"--backup-dir={os.path.join(dest, '.backup-'+timestamp)}"
    ]
    if dry_run:
        rsync_opts.append("--dry-run")
        logging.info("Running in DRY RUN mode...")
    # Include exclude file if exists
    if os.path.isfile(EXCLUDE_FILE):
        rsync_opts.append(f"--exclude-from={EXCLUDE_FILE}")
    # Assemble rsync command
    cmd = ["rsync"] + rsync_opts + [os.path.join(source, ""), os.path.join(dest, "")]
    # Run rsync and log output
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        logging.error(f"Failed to run rsync: {e}")
        sys.exit(1)
    rsync_output = result.stdout
    if rsync_output:
        logging.info("\n" + rsync_output.strip())
    end_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if result.returncode == 0:
        logging.info(f"rsync completed at {end_time}")
    else:
        logging.error(f"rsync exited with errors (exit code {result.returncode}) at {end_time}")
        sys.exit(result.returncode)
