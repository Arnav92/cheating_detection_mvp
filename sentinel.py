#!/usr/bin/env python3
"""
Sentinel telemetry script that records coding activity.
Compares current src/ against .sentinel_state.json to detect changes.
Records chars_added, time_delta, velocity, and is_suspicious flag.
"""

import json
import os
import sys
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path


def get_username():
    """Get the current git username or system username."""
    try:
        import subprocess
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


def get_src_content(src_dir):
    """
    Get all content from src/ directory recursively.
    
    Args:
        src_dir: Path to src directory
    
    Returns:
        Dictionary mapping file paths to their content
    """
    content = {}
    src_path = Path(src_dir)
    
    if not src_path.exists():
        return content
    
    for file_path in src_path.rglob('*'):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    relative_path = str(file_path.relative_to(src_path))
                    content[relative_path] = f.read()
            except (UnicodeDecodeError, IOError):
                # Skip binary files or files we can't read
                pass
    
    return content


def calculate_chars_added(old_content, new_content):
    """
    Calculate the number of characters added between old and new content.
    
    Args:
        old_content: Dictionary of old file contents
        new_content: Dictionary of new file contents
    
    Returns:
        Total number of characters added
    """
    chars_added = 0
    
    # Check all new files
    for file_path, content in new_content.items():
        old = old_content.get(file_path, '')
        new_chars = len(content)
        old_chars = len(old)
        
        if new_chars > old_chars:
            chars_added += new_chars - old_chars
    
    return chars_added


def main():
    """Main sentinel function."""
    try:
        # Define paths
        project_dir = Path(__file__).parent
        src_dir = project_dir / 'src'
        state_file = project_dir / '.sentinel_state.json'
        telemetry_file = project_dir / 'telemetry.jsonl'
        
        # Get current src/ content
        current_content = get_src_content(src_dir)
        current_time = time.time()
        
        # Load previous state
        old_content = {}
        old_time = current_time
        
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    old_content = state.get('content', {})
                    old_time = state.get('timestamp', current_time)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Calculate metrics
        chars_added = calculate_chars_added(old_content, current_content)
        time_delta = max(current_time - old_time, 1)  # Avoid division by zero
        velocity = chars_added / time_delta  # chars per second
        is_suspicious = velocity > 50
        
        # Create telemetry entry
        entry = {
            'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'user': get_username(),
            'chars_added': chars_added,
            'time_delta': round(time_delta, 2),
            'velocity': round(velocity, 2),
            'is_suspicious': is_suspicious
        }
        
        # Append to telemetry.jsonl (JSONL format: one JSON object per line)
        with open(telemetry_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Update state
        new_state = {
            'timestamp': current_time,
            'content': current_content
        }
        
        with open(state_file, 'w') as f:
            json.dump(new_state, f)
        
        # Always exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Silently fail - never break the build
        sys.exit(0)


if __name__ == '__main__':
    main()
