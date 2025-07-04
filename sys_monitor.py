#!/usr/bin/env python3
"""
sys_monitor.py - System Monitoring: Display system uptime, resource utilization, and top processes.

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
    sys_monitor.py    (no arguments)

Description:
    Shows system uptime and load averages, memory usage, disk usage, 
    and the top 5 processes by CPU and memory usage.
"""
import sys
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        logging.error("Usage: sys_monitor.py (no arguments)")
        sys.exit(1)
    # Uptime and Load
    logging.info("==== System Uptime and Load ====")
    try:
        uptime_out = subprocess.check_output(["uptime"], text=True).strip()
    except Exception as e:
        uptime_out = ""
        logging.error(f"Could not retrieve uptime: {e}")
    if uptime_out:
        logging.info(uptime_out)
    # Memory Usage
    logging.info("\n==== Memory Usage ====")
    try:
        free_out = subprocess.check_output(["free", "-h"], text=True).strip()
    except Exception as e:
        free_out = ""
        logging.error(f"Could not retrieve memory info: {e}")
    if free_out:
        # Only display the header and first line of memory data for brevity
        lines = free_out.splitlines()
        if lines:
            logging.info("\n" + "\n".join(lines[:2]))
    # Disk Usage
    logging.info("\n==== Disk Usage ====")
    try:
        df_out = subprocess.check_output(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], text=True).strip()
    except Exception as e:
        df_out = ""
        logging.error(f"Could not retrieve disk usage: {e}")
    if df_out:
        logging.info("\n" + df_out)
    # Top CPU processes
    logging.info("\n==== Top 5 CPU-consuming processes ====")
    try:
        ps_cpu = subprocess.check_output(
            ["ps", "-eo", "pid,user,comm,%cpu", "--sort=-%cpu"], text=True
        ).strip().splitlines()
    except Exception as e:
        ps_cpu = []
        logging.error(f"Failed to get process list: {e}")
    if ps_cpu:
        top_cpu = "\n".join(ps_cpu[:6])
        logging.info("\n" + top_cpu)
    # Top Memory processes
    logging.info("\n==== Top 5 Memory-consuming processes ====")
    try:
        ps_mem = subprocess.check_output(
            ["ps", "-eo", "pid,user,comm,%mem", "--sort=-%mem"], text=True
        ).strip().splitlines()
    except Exception as e:
        ps_mem = []
        logging.error(f"Failed to get process list: {e}")
    if ps_mem:
        top_mem = "\n".join(ps_mem[:6])
        logging.info("\n" + top_mem)
