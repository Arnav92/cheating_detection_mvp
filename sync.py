#!/usr/bin/env python3
"""
Sync script that pushes telemetry data to a remote git repository.
Clones the cheat_logging repo to ~/.cheat_logs, copies telemetry.jsonl as {git_username}.jsonl,
and performs silent background git operations.
"""

import json
import os
import subprocess
import sys
import shlex
from pathlib import Path


def get_username():
    """Get the current git username or system username."""
    try:
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'


def sync_telemetry():
    """
    Sync telemetry data to remote git repository.
    Uses subprocess.Popen for background operations to avoid blocking the build.
    """
    try:
        # Paths
        logs_dir = Path.home() / '.cheat_logs'
        project_dir = Path(__file__).parent
        telemetry_file = project_dir / 'telemetry.jsonl'
        repo_url = 'https://github.com/Arnav92/cheat_logging.git'
        username = get_username()
        
        # Check if telemetry file exists
        if not telemetry_file.exists():
            # No data to sync, silently exit
            sys.exit(0)
        
        # Clone repository if it doesn't exist
        if not logs_dir.exists():
            try:
                subprocess.run(
                    ['git', 'clone', repo_url, str(logs_dir)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=30
                )
            except Exception:
                # Clone failed, silently exit
                sys.exit(0)
        
        # Read telemetry data
        try:
            with open(telemetry_file, 'r') as f:
                telemetry_data = f.read()
        except IOError:
            sys.exit(0)
        
        # Write/append to user's log file
        user_log_file = logs_dir / f'{username}.jsonl'
        try:
            with open(user_log_file, 'a') as f:
                f.write(telemetry_data)
        except IOError:
            sys.exit(0)
        
        # Prepare git sync commands
        sync_commands = [
            ['git', '-C', str(logs_dir), 'add', '.'],
            ['git', '-C', str(logs_dir), 'commit', '-m', 'update'],
            ['git', '-C', str(logs_dir), 'pull', '--rebase'],
            ['git', '-C', str(logs_dir), 'push'],
        ]
        
        # Execute sync commands synchronously (will block for a few seconds)
        try:
            for cmd in sync_commands:
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
        except Exception:
            # Silently ignore any git errors
            pass
        
        # Clear local telemetry file after initiating sync
        try:
            telemetry_file.unlink()
        except Exception:
            pass
        
        # Always exit successfully
        sys.exit(0)
        
    except Exception:
        # Silently fail - never break the build
        sys.exit(0)


if __name__ == '__main__':
    sync_telemetry()
