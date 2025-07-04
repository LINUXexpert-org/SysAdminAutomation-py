#!/usr/bin/env python3
"""
security_audit.py - Security Audit: Check for common security issues (permissions, open ports).

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
    security_audit.py    (no arguments)

Description:
    Lists world-writable files, world-writable directories without sticky bit, SUID/SGID files, and open listening ports.
"""
import sys
import os
import stat
import shutil
import subprocess
import logging
from pwd import getpwuid
from grp import getgrgid

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def list_world_writable_files():
    logging.info("==== World-Writable Files (potentially unsafe) ====")
    count = 0
    for root, dirs, files in os.walk("/"):
        # Skip traversal into other filesystems (like /proc, /sys) using -xdev logic:
        # Stop descending into mount points by skipping known virtual file systems
        if root in ["/proc", "/sys", "/run", "/dev"]:
            dirs[:] = []
            continue
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                st = os.stat(fpath)
            except Exception:
                continue
            # Check if world-writable (others have write permission)
            if st.st_mode & 0o002:
                # Get permission string, owner, group
                perm_str = stat.filemode(st.st_mode)
                try:
                    owner = getpwuid(st.st_uid).pw_name
                except KeyError:
                    owner = st.st_uid
                try:
                    group = getgrgid(st.st_gid).gr_name
                except KeyError:
                    group = st.st_gid
                logging.info(f"{perm_str} {owner} {group} {fpath}")
                count += 1
    # (If none found, nothing will be logged under the header)

def list_world_writable_dirs_no_sticky():
    logging.info("\n==== World-Writable Directories (no sticky bit) ====")
    count = 0
    for root, dirs, files in os.walk("/"):
        if root in ["/proc", "/sys", "/run", "/dev"]:
            dirs[:] = []
            continue
        for dname in dirs:
            dpath = os.path.join(root, dname)
            try:
                st = os.stat(dpath)
            except Exception:
                continue
            # Check if directory is world-writable and lacks the sticky bit
            if stat.S_ISDIR(st.st_mode) and (st.st_mode & 0o002) and not (st.st_mode & 0o1000):
                perm_str = stat.filemode(st.st_mode)
                try:
                    owner = getpwuid(st.st_uid).pw_name
                except KeyError:
                    owner = st.st_uid
                try:
                    group = getgrgid(st.st_gid).gr_name
                except KeyError:
                    group = st.st_gid
                logging.info(f"{perm_str} {owner} {group} {dpath}")
                count += 1

def list_suid_sgid_files():
    logging.info("\n==== SUID/SGID Files ====")
    count = 0
    for root, dirs, files in os.walk("/"):
        if root in ["/proc", "/sys", "/run", "/dev"]:
            dirs[:] = []
            continue
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                st = os.stat(fpath)
            except Exception:
                continue
            # Check for SUID or SGID bit
            if st.st_mode & 0o4000 or st.st_mode & 0o2000:
                perm_str = stat.filemode(st.st_mode)
                try:
                    owner = getpwuid(st.st_uid).pw_name
                except KeyError:
                    owner = st.st_uid
                try:
                    group = getgrgid(st.st_gid).gr_name
                except KeyError:
                    group = st.st_gid
                logging.info(f"{perm_str} {owner} {group} {fpath}")
                count += 1

def list_open_ports():
    logging.info("\n==== Listening Network Ports ====")
    # Use ss or netstat to list open ports
    if shutil.which("ss"):
        try:
            output = subprocess.check_output(["ss", "-tulwn"], text=True).strip()
        except subprocess.CalledProcessError as e:
            output = ""
        if output:
            logging.info("\n" + output)
        else:
            logging.info("(No listening ports or 'ss' produced no output)")
    elif shutil.which("netstat"):
        try:
            output = subprocess.check_output(["netstat", "-tuln"], text=True).strip()
        except subprocess.CalledProcessError as e:
            output = ""
        if output:
            logging.info("\n" + output)
        else:
            logging.info("(No listening ports or 'netstat' produced no output)")
    else:
        logging.info("No command available to list network ports.")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        logging.error("Usage: security_audit.py (no arguments)")
        sys.exit(1)
    list_world_writable_files()
    list_world_writable_dirs_no_sticky()
    list_suid_sgid_files()
    list_open_ports()
