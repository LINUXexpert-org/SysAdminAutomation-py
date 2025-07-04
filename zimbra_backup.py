#!/usr/bin/env python3
"""
zimbra_backup.py - Backup a Zimbra mailbox to a TGZ file.

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
    zimbra_backup.py    (interactive, prompts for email and backup directory)

Description:
    Runs an interactive prompt to get a Zimbra email account and backup directory, then uses Zimbra's zmmailbox tool to export the mailbox to a .tgz file.
"""
import os
import subprocess
import getpass
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    # Prompt for input
    email = input("Enter Zimbra username (email address): ").strip()
    backup_dir = input("Enter backup directory (absolute path) [/opt/zimbra/backups]: ").strip()
    if backup_dir == "":
        backup_dir = "/opt/zimbra/backups"
    # Ensure directory exists and ownership
    os.makedirs(backup_dir, exist_ok=True)
    try:
        # Change owner to zimbra:zimbra
        import pwd, grp
        uid = pwd.getpwnam("zimbra").pw_uid
        gid = grp.getgrnam("zimbra").gr_gid
        os.chown(backup_dir, uid, gid)
    except Exception as e:
        logging.warning(f"Could not change owner of {backup_dir} to zimbra:zimbra (proceeding anyway): {e}")
    # Generate backup filename
    from datetime import datetime
    timestamp = datetime.now().strftime("%F_%H-%M-%S")
    backup_file = os.path.join(backup_dir, f"{email}_{timestamp}.tgz")
    # Confirm action
    confirm = input(f"Backing up mailbox for {email} to {backup_file}\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        logging.info("Backup cancelled.")
        exit(0)
    logging.info("Starting backup...")
    # Run zmmailbox as zimbra user
    cmd = ["sudo", "-u", "zimbra", "bash", "-c",
           f"/opt/zimbra/bin/zmmailbox -z -m '{email}' getRestURL '//?fmt=tgz' > '{backup_file}'"]
    result = subprocess.run(" ".join(cmd), shell=True)
    if result.returncode == 0:
        logging.info(f"✅ Backup completed: {backup_file}")
    else:
        # If failed, remove incomplete file
        if os.path.exists(backup_file):
            os.remove(backup_file)
        logging.error("❌ Backup failed. Check if the user exists or zmmailbox is working.")
except KeyboardInterrupt:
    print("\nOperation cancelled by user.")
