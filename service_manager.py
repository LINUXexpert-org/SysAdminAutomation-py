#!/usr/bin/env python3
"""
service_manager.py - Service Management: Start, stop, restart, check status, or enable/disable system services.

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
    service_manager.py <start|stop|restart|status|enable|disable> <service_name>

Description:
    Controls system services by invoking the appropriate system service manager (systemctl or service).
    For "status", it will display the service status. "enable" or "disable" will configure the service to start at boot or not.
"""
import sys
import shutil
import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

VALID_ACTIONS = {"start", "stop", "restart", "status", "enable", "disable"}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in VALID_ACTIONS:
        logging.error(f"Usage: {sys.argv[0]} <start|stop|restart|status|enable|disable> <service_name>")
        sys.exit(1)
    action = sys.argv[1]
    service = sys.argv[2]

    # Suggest root for actions that modify service state
    if action in {"start", "stop", "restart", "enable", "disable"}:
        if os.name != 'nt':
            try:
                if os.geteuid() != 0:
                    logging.warning("This action may require root privileges to succeed.")
            except AttributeError:
                pass

    # Determine command (systemctl or service)
    if shutil.which("systemctl"):
        cmd = ["systemctl", action, service]
    elif shutil.which("service"):
        # Map enable/disable to SysVinit equivalent if needed (enable/disable might not exist for 'service')
        if action in {"enable", "disable"}:
            logging.error("Enable/disable not supported with this service manager.")
            sys.exit(1)
        cmd = ["service", service, action]
    else:
        logging.error("No service management tool found (systemctl or service).")
        sys.exit(1)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        logging.error(f"Failed to execute service command: {e}")
        sys.exit(1)

    # Output handling
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    if action == "status":
        if stdout:
            logging.info(stdout)
        if stderr:
            # systemctl status may use stderr for some output
            logging.info(stderr)
        if result.returncode != 0:
            logging.error(f"Service '{service}' status check failed (exit code {result.returncode}).")
            sys.exit(result.returncode)
    else:
        if result.returncode == 0:
            # For start/stop/restart/enable/disable, print a success message
            logging.info(f"Service '{service}' {action}ed successfully.")
        else:
            # If there is error output, include it in the error message
            if stderr or stdout:
                logging.error(f"Failed to {action} service '{service}'. Output:\n{stderr or stdout}")
            else:
                logging.error(f"Failed to {action} service '{service}'. (Exit code {result.returncode})")
            sys.exit(result.returncode)
