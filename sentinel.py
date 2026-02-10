#!/usr/bin/env python3
"""
Sentinel telemetry script that records coding activity.
Records timestamp, user, chars_added, and velocity to a hidden local JSON.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


def get_username():
    """Get the current system username."""
    return os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'


def calculate_velocity(chars_added, time_elapsed):
    """Calculate typing velocity (chars per minute)."""
    if time_elapsed == 0:
        return 0
    return (chars_added / time_elapsed) * 60


def record_telemetry(chars_added=0, time_elapsed=1):
    """
    Record telemetry data to hidden local JSON file.
    
    Args:
        chars_added: Number of characters added
        time_elapsed: Time elapsed in seconds
    """
    # Hidden file in home directory
    telemetry_file = Path.home() / '.telemetry.json'
    
    # Create telemetry entry
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'user': get_username(),
        'chars_added': chars_added,
        'velocity': round(calculate_velocity(chars_added, time_elapsed), 2)
    }
    
    # Read existing data
    data = []
    if telemetry_file.exists():
        try:
            with open(telemetry_file, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = []
    
    # Append new entry
    data.append(entry)
    
    # Write back to file
    with open(telemetry_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Telemetry recorded: {entry}")


if __name__ == '__main__':
    # Example usage: record a sample telemetry entry
    # In a real scenario, this would be called with actual metrics
    record_telemetry(chars_added=100, time_elapsed=10)
