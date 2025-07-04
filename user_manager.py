#!/usr/bin/env python3
"""
user_manage.py - User and Group Management: Create/remove users and groups, modify memberships, lock/unlock accounts.

Usage:
    user_manage.py adduser <username> [group]
    user_manage.py deluser <username>
    user_manage.py addgroup <group>
    user_manage.py delgroup <group>
    user_manage.py addtogroup <username> <group>
    user_manage.py removefromgroup <username> <group>
    user_manage.py lock <username>
    user_manage.py unlock <username>

Description:
    Provides user and group management operations. Must be run as root for most actions.
"""
import sys
import shutil
import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Define expected commands for user management
ACTIONS = ["adduser", "deluser", "addgroup", "delgroup", "addtogroup", "removefromgroup", "lock", "unlock"]

def run_cmd(cmd_list):
    """Run a system command and handle errors."""
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True)
    except Exception as e:
        logging.error(f"Failed to execute command {' '.join(cmd_list)}: {e}")
        sys.exit(1)
    if result.returncode != 0:
        # Include any error output in the log
        err_msg = (result.stderr or result.stdout).strip()
        logging.error(f"Command {' '.join(cmd_list)} failed: {err_msg}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logging.error(f"Usage: {sys.argv[0]} <action> <name> [extra]")
        sys.exit(1)
    action = sys.argv[1]
    if action not in ACTIONS:
        logging.error(f"Unknown action: {action}")
        sys.exit(1)
    # Suggest running as root for actions that require it
    if os.name != 'nt':
        try:
            if os.geteuid() != 0:
                logging.warning("This operation likely requires root privileges.")
        except AttributeError:
            pass

    if action == "adduser":
        # Usage: adduser <username> [initial_group]
        username = sys.argv[2]
        initial_group = sys.argv[3] if len(sys.argv) > 3 else None
        cmd = ["useradd", "-m", username]
        if initial_group:
            cmd += ["-G", initial_group]
        run_cmd(cmd)
        logging.info(f"User '{username}' added successfully.")
    elif action == "deluser":
        username = sys.argv[2]
        run_cmd(["userdel", "-r", username])
        logging.info(f"User '{username}' removed successfully.")
    elif action == "addgroup":
        group = sys.argv[2]
        run_cmd(["groupadd", group])
        logging.info(f"Group '{group}' created successfully.")
    elif action == "delgroup":
        group = sys.argv[2]
        run_cmd(["groupdel", group])
        logging.info(f"Group '{group}' removed successfully.")
    elif action == "addtogroup":
        if len(sys.argv) < 4:
            logging.error(f"Usage: {sys.argv[0]} addtogroup <username> <group>")
            sys.exit(1)
        username = sys.argv[2]; group = sys.argv[3]
        run_cmd(["usermod", "-a", "-G", group, username])
        logging.info(f"User '{username}' added to group '{group}'.")
    elif action == "removefromgroup":
        if len(sys.argv) < 4:
            logging.error(f"Usage: {sys.argv[0]} removefromgroup <username> <group>")
            sys.exit(1)
        username = sys.argv[2]; group = sys.argv[3]
        run_cmd(["gpasswd", "-d", username, group])
        logging.info(f"User '{username}' removed from group '{group}'.")
    elif action == "lock":
        username = sys.argv[2]
        run_cmd(["usermod", "-L", username])
        logging.info(f"User '{username}' account locked.")
    elif action == "unlock":
        username = sys.argv[2]
        run_cmd(["usermod", "-U", username])
        logging.info(f"User '{username}' account unlocked.")
