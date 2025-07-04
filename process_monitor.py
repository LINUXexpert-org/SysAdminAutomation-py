#!/usr/bin/env python3
"""
process_monitor.py - Process Management: List top processes and allow termination by name or PID.

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
    process_monitor.py            (shows top CPU & memory processes)
    process_monitor.py kill <process_name|PID>

Description:
    Without arguments, displays the top 5 CPU-consuming and top 5 memory-consuming processes.
    With "kill", terminates the specified process by PID or by exact name.
"""
import sys
import os
import signal
import subprocess
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def list_top_processes():
    """List top 5 processes by CPU and memory usage."""
    logging.info("==== Top 5 CPU-consuming processes ====")
    try:
        ps_cpu = subprocess.check_output(
            ["ps", "-eo", "pid,user,comm,%cpu", "--sort=-%cpu"], text=True
        ).strip().splitlines()
    except Exception as e:
        logging.error(f"Failed to retrieve process list: {e}")
        return
    if ps_cpu:
        lines = ps_cpu[:6]  # first line is header, next 5 lines are top processes
        logging.info("\n" + "\n".join(lines))
    logging.info("\n==== Top 5 Memory-consuming processes ====")
    try:
        ps_mem = subprocess.check_output(
            ["ps", "-eo", "pid,user,comm,%mem", "--sort=-%mem"], text=True
        ).strip().splitlines()
    except Exception as e:
        logging.error(f"Failed to retrieve process list: {e}")
        return
    if ps_mem:
        lines = ps_mem[:6]
        logging.info("\n" + "\n".join(lines))

def kill_process(target: str):
    """Kill a process by PID or by exact name."""
    # Determine if target is PID (all digits) or name
    if re.fullmatch(r"\d+", target):
        pid = int(target)
        try:
            os.kill(pid, signal.SIGTERM)
            logging.info(f"Process {pid} killed.")
        except Exception as e:
            logging.error(f"Failed to kill process {pid}: {e}")
            sys.exit(1)
    else:
        # Kill by name (exact match)
        if shutil.which("pkill"):
            result = subprocess.run(["pkill", "-x", target])
            if result.returncode == 0:
                logging.info(f"Processes named '{target}' killed.")
            else:
                logging.error(f"No process '{target}' found or kill failed.")
                sys.exit(1)
        else:
            # If pkill not available, attempt manual approach
            killed_any = False
            try:
                ps_output = subprocess.check_output(["ps", "-Ao", "pid,comm"], text=True)
            except Exception as e:
                logging.error(f"Failed to list processes: {e}")
                sys.exit(1)
            for line in ps_output.splitlines():
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    pid_str, name = parts
                    if name == target:
                        try:
                            os.kill(int(pid_str), signal.SIGTERM)
                            killed_any = True
                        except Exception:
                            pass
            if killed_any:
                logging.info(f"Processes named '{target}' killed.")
            else:
                logging.error(f"No process '{target}' found or kill failed.")
                sys.exit(1)

if __name__ == "__main__":
    import shutil
    if len(sys.argv) == 1:
        # No arguments: show top processes
        list_top_processes()
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "kill":
        target = sys.argv[2]
        if not target:
            logging.error(f"Usage: {sys.argv[0]} kill <process_name|PID>")
            sys.exit(1)
        kill_process(target)
    else:
        logging.error(f"Usage: {sys.argv[0]} [kill <process_name|PID>]")
        sys.exit(1)
