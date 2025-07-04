#!/usr/bin/env python3
"""
zimbra_restore.py - Restore a Zimbra mailbox from a backup TGZ.

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
    zimbra_restore.py    (interactive prompts for details)

Description:
    Prompts for the target email account and backup file, then uses Zimbra's zmmailbox to restore the mailbox data.
"""
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    email = input("Enter Zimbra username to restore to (email address): ").strip()
    backup_dir = input("Enter backup directory (absolute path) [/opt/zimbra/backups]: ").strip()
    if backup_dir == "":
        backup_dir = "/opt/zimbra/backups"
    filename = input("Enter the exact filename of the backup to restore (e.g., user@example.com_YYYY-MM-DD_HH-MM-SS.tgz): ").strip()
    full_path = os.path.join(backup_dir, filename)
    # Verify backup file exists
    if not os.path.isfile(full_path):
        logging.error(f"❌ Backup file not found: {full_path}")
        exit(1)
    # Warning confirmation
    confirm = input(f"⚠️ You are about to restore {full_path} into {email}'s mailbox.\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        logging.info("Restore cancelled.")
        exit(0)
    logging.info("Restoring backup...")
    # Run zmmailbox restore as zimbra user
    cmd = ["sudo", "-u", "zimbra", "bash", "-c",
           f"/opt/zimbra/bin/zmmailbox -z -m '{email}' postRestURL '/?fmt=tgz&resolve=skip' --file '{full_path}'"]
    result = subprocess.run(" ".join(cmd), shell=True)
    if result.returncode == 0:
        logging.info(f"✅ Restore completed successfully for {email}")
    else:
        logging.error("❌ Restore failed. Please verify mailbox exists and backup file integrity.")
except KeyboardInterrupt:
    print("\nOperation cancelled by user.")
