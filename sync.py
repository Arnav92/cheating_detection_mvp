#!/usr/bin/env python3
"""
Sync script that pushes telemetry data to a remote git repository.
Clones the cheat_logging repo, copies local JSON as {user}.jsonl, and pushes changes.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def get_username():
    """Get the current system username."""
    return os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'


def run_command(cmd, cwd=None, silent=True):
    """
    Run a shell command.
    
    Args:
        cmd: Command to run (string or list)
        cwd: Working directory
        silent: Whether to suppress output
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if silent:
            subprocess.run(
                cmd,
                cwd=cwd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=isinstance(cmd, str)
            )
        else:
            subprocess.run(
                cmd,
                cwd=cwd,
                check=True,
                shell=isinstance(cmd, str)
            )
        return True
    except subprocess.CalledProcessError:
        return False


def sync_telemetry():
    """
    Sync telemetry data to remote git repository.
    Note: This requires git credentials configured for push access.
    For production use, configure SSH keys or credential helper.
    """
    # Paths
    logs_dir = Path.home() / '.logs'
    telemetry_file = Path.home() / '.telemetry.json'
    repo_url = 'https://github.com/Arnav92/cheat_logging.git'
    username = get_username()
    
    # Check if telemetry file exists
    if not telemetry_file.exists():
        print("No telemetry data to sync.")
        return
    
    # Clone repository if it doesn't exist
    if not logs_dir.exists():
        print(f"Cloning repository to {logs_dir}...")
        if not run_command(['git', 'clone', repo_url, str(logs_dir)], silent=True):
            print(f"Failed to clone repository from {repo_url}")
            return
    
    # Read telemetry data
    try:
        with open(telemetry_file, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading telemetry file: {e}")
        return
    
    # Write as JSONL (one JSON object per line)
    user_log_file = logs_dir / f'{username}.jsonl'
    try:
        with open(user_log_file, 'a') as f:
            for entry in data:
                f.write(json.dumps(entry) + '\n')
    except IOError as e:
        print(f"Error writing to log file: {e}")
        return
    
    # Git operations
    print("Syncing to remote repository...")
    
    # Add file
    run_command(['git', 'add', f'{username}.jsonl'], cwd=logs_dir, silent=True)
    
    # Commit (only if there are changes)
    run_command(
        ['git', 'commit', '-m', f'Update telemetry for {username}'],
        cwd=logs_dir,
        silent=True
    )
    
    # Pull with rebase and push
    if run_command(['git', 'pull', '--rebase'], cwd=logs_dir, silent=True):
        if run_command(['git', 'push'], cwd=logs_dir, silent=True):
            print("Telemetry synced successfully.")
            # Clear local telemetry file after successful sync
            try:
                with open(telemetry_file, 'w') as f:
                    json.dump([], f)
            except IOError as e:
                print(f"Warning: Failed to clear telemetry file: {e}")
        else:
            print("Failed to push changes.")
    else:
        print("Failed to pull changes.")


if __name__ == '__main__':
    sync_telemetry()
