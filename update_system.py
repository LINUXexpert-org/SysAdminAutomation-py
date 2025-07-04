#!/usr/bin/env python3
"""
update_system.py - System Updates: Apply available package updates for various Linux package managers.

Usage:
    update_system.py    (no arguments)

Description:
    Detects the system's package manager (apt, yum/dnf, zypper, pacman) and applies all available updates.
    Must be run with appropriate privileges (usually as root).
"""
import sys
import shutil
import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        logging.error("Usage: update_system.py (no arguments)")
        sys.exit(1)
    # Ensure running as root (for Unix-like systems)
    if os.name != 'nt':
        try:
            if os.geteuid() != 0:
                logging.warning("This script should be run as root to apply system updates.")
        except AttributeError:
            pass

    # Identify package manager and run updates
    try:
        if shutil.which("apt-get"):
            logging.info("Updating package lists (apt-get)...")
            subprocess.run(["apt-get", "update"], check=True)
            logging.info("Upgrading packages (apt-get)...")
            subprocess.run(["apt-get", "-y", "upgrade"], check=True)
        elif shutil.which("dnf"):
            logging.info("Upgrading packages (dnf)...")
            subprocess.run(["dnf", "-y", "upgrade"], check=True)
        elif shutil.which("yum"):
            logging.info("Updating packages (yum)...")
            subprocess.run(["yum", "-y", "update"], check=True)
        elif shutil.which("zypper"):
            logging.info("Refreshing repositories (zypper)...")
            subprocess.run(["zypper", "--non-interactive", "refresh"], check=True)
            logging.info("Upgrading packages (zypper)...")
            subprocess.run(["zypper", "--non-interactive", "update"], check=True)
        elif shutil.which("pacman"):
            logging.info("Upgrading packages (pacman)...")
            subprocess.run(["pacman", "-Syu", "--noconfirm"], check=True)
        else:
            logging.error("No supported package manager found on this system.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Package update failed: {e}")
        sys.exit(e.returncode)

    logging.info("System update completed successfully.")
