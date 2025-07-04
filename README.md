# Linux System Administration Scripts

Automate routine tasks: This project provides a collection of Python scripts to automate common Linux system administration duties. Automating daily sysadmin tasks improves efficiency and consistency by reducing manual repetition and the risk of human error. Each script is designed to be distribution-agnostic, using only standard base utilities (e.g. rsync, tar, awk, grep, netstat/ss, systemctl) available on most Linux systems. All scripts are released under the GNU GPL v3.0 license and include usage information in their headers.

## Included Scripts

- `backup.py` – Backup Utility: Archive directories into compressed tarballs for backups.
- `restore.py` – Restore Utility: Restore files from backup archives.
- `disk_cleanup.py` – Disk Usage & Cleanup: Report disk usage and identify large files; optionally clean package caches and temporary files to free space.
- `log_inspect.py` – Log Inspection: Search within log files or tail the latest system logs for troubleshooting.
- `log_rotate.py` – Log Rotation: Compress and rotate old log files to prevent excessive disk usage
- `network_info.py` – Network & Firewall Info: Show network interface details, routing table, open listening ports, and basic firewall (iptables) rules.
- `process_monitor.py` – Process Management: List top resource-consuming processes and allow termination of processes by name or PID.
- `security_audit.py`– Security Audit: Scan for security issues like world-writable files, SUID/SGID executables, and open network ports.
- `service_manager.py`– Service Management: Start, stop, restart, or check status of system services, and enable/disable services at boot.
- `sys_monitor.py` – System Monitoring: Display system uptime, resource utilization (CPU, memory, disk), and top processes.
- `update_system.py` – System Updates: Apply available package updates and patches (works with apt, yum/dnf, zypper, pacman).
- `user_manage.py`  – User and Group Management: Create or remove user accounts and groups, modify user group memberships, and lock/unlock accounts.
- `zimbra_backup.py`  - Create a backup for a zimbra mailbox.
- `zimbra_restore.py`  - Restore a backup for a zimbra mailbox.
- `rsync_magic.py`  -  A smart Bash script that wraps rsync for safe, flexible, and efficient file synchronization and backups.
