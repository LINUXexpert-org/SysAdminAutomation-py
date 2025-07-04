#!/usr/bin/env python3
"""
network_info.py - Network & Firewall Info: Show network interfaces, routes, open ports, and firewall rules.

Usage:
    network_info.py    (no arguments)

Description:
    Displays network interface addresses, routing table, open listening ports, and basic firewall (iptables) rules.
"""
import sys
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_and_log(cmd, section_name):
    """Run a shell command and log its output under a section heading."""
    logging.info(section_name)
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        logging.error(f"Failed to run command {cmd}: {e}")
        return
    output = result.stdout.strip()
    if output:
        # Log output as multiline (single log entry)
        logging.info("\n" + output)
    if result.returncode != 0:
        # If command failed, include stderr output or error note
        err = result.stderr.strip()
        if err:
            logging.warning(f"(Command error output: {err})")
        else:
            logging.warning(f"(Command {cmd} exited with code {result.returncode})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        logging.error("Usage: network_info.py (no arguments)")
        sys.exit(1)
    # Network Interfaces (IP addresses)
    logging.info("==== Network Interfaces (IP addresses) ====")
    if shutil.which("ip"):
        run_and_log(["ip", "-brief", "addr", "show"], "")
    elif shutil.which("ifconfig"):
        run_and_log(["ifconfig", "-a"], "")
    else:
        logging.info("No network interface tool (ip or ifconfig) available.")
    # Routing Table
    logging.info("\n==== Routing Table ====")
    if shutil.which("ip"):
        run_and_log(["ip", "route", "show"], "")
    elif shutil.which("route"):
        run_and_log(["route", "-n"], "")
    else:
        logging.info("No routing tool (ip or route) available.")
    # Listening Ports (TCP/UDP)
    logging.info("\n==== Listening Ports (TCP/UDP) ====")
    if shutil.which("ss"):
        run_and_log(["ss", "-tulwn"], "")
    elif shutil.which("netstat"):
        run_and_log(["netstat", "-tuln"], "")
    else:
        logging.info("No socket listing tool (ss or netstat) available.")
    # Firewall Rules (iptables)
    logging.info("\n==== Firewall Rules (iptables) ====")
    if shutil.which("iptables"):
        run_and_log(["iptables", "-L", "-n", "-v"], "")
    else:
        logging.info("iptables command not found (no firewall rules to show or using nftables).")
