#!/usr/bin/env python3
"""
log_inspect.py - Log Inspection: Search within logs or tail log files.

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
    log_inspect.py search <pattern>
    log_inspect.py tail <log_file_path>
    log_inspect.py             (default: tail system log)

Description:
    Searches across /var/log for a given pattern (case-insensitive), or tails the specified log file.
    With no arguments, tails the last 50 lines of the system syslog or messages file.
"""
import sys
import os
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def search_logs(pattern: str):
    """Recursively search for pattern (case-insensitive) in all files under /var/log."""
    logging.info(f"Searching for '{pattern}' in /var/log...")
    regex = re.compile(re.escape(pattern), re.IGNORECASE)
    matches_found = 0
    for root, dirs, files in os.walk("/var/log"):
        for fname in files:
            file_path = os.path.join(root, fname)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    for line in f:
                        if regex.search(line):
                            # Print file path and matching line
                            logging.info(f"{file_path}: {line.strip()}")
                            matches_found += 1
            except Exception:
                continue  # skip files that can't be opened
    if matches_found == 0:
        logging.info("No matches found.")

def tail_file(log_path: str, lines: int = 100):
    """Display the last `lines` lines of the given logfile."""
    if not os.path.isfile(log_path):
        logging.error(f"Log file '{log_path}' not found.")
        sys.exit(1)
    try:
        with open(log_path, "r") as f:
            all_lines = f.readlines()
    except Exception as e:
        logging.error(f"Could not read log file '{log_path}': {e}")
        sys.exit(1)
    start = -lines if len(all_lines) >= lines else 0
    snippet = "".join(all_lines[start:])
    logging.info(f"== Last {lines} lines of {log_path} ==\n{snippet.strip()}")

def tail_default_system_log():
    """Tail the system's main log (syslog or messages) for the last 50 lines."""
    syslog = "/var/log/syslog"
    messages = "/var/log/messages"
    if os.path.isfile(syslog):
        log_path = syslog
    elif os.path.isfile(messages):
        log_path = messages
    else:
        logging.warning("No syslog or messages log found.")
        return
    tail_file(log_path, lines=50)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        mode = sys.argv[1].lower()
        if mode == "search":
            if len(sys.argv) < 3:
                logging.error(f"Usage: {sys.argv[0]} search <pattern>")
                sys.exit(1)
            search_logs(sys.argv[2])
            sys.exit(0)
        elif mode == "tail":
            if len(sys.argv) < 3:
                logging.error(f"Usage: {sys.argv[0]} tail <log_file_path>")
                sys.exit(1)
            tail_file(sys.argv[2], lines=100)
            sys.exit(0)
        # If mode not recognized, fall through to default behavior
    # Default behavior (no or unknown args): tail system log
    tail_default_system_log()
