# Cheating Detection MVP

A telemetry system for tracking coding velocity and detecting suspicious activity in university coding exercises. This system silently monitors student coding patterns and reports potential cheating attempts.

## Overview

This MVP integrates into a Java/Gradle build process to:
- Track coding velocity (characters added per second)
- Detect suspicious activity (velocity > 50 chars/sec)
- Silently push telemetry logs to a central repository
- Never interfere with or fail student builds

## Architecture

### Components

1. **sentinel.py** - Tracks coding activity
   - Compares current `src/` directory against `.sentinel_state.json`
   - Calculates `chars_added`, `time_delta`, and `velocity`
   - Flags suspicious activity when velocity > 50 chars/sec
   - Appends data to `telemetry.jsonl`
   - Always exits with code 0

2. **sync.py** - Syncs telemetry to central repository
   - Clones `https://github.com/Arnav92/cheat_logging.git` to `~/.cheat_logs`
   - Copies `telemetry.jsonl` to `{git_username}.jsonl` in the repo
   - Performs background git operations using `subprocess.Popen`
   - All git output redirected to `/dev/null` for stealth
   - Always exits with code 0

3. **build.gradle** - Build integration
   - Defines `telemetry` task that runs sentinel.py and sync.py
   - `compileJava.dependsOn telemetry` ensures it runs on every build
   - All output suppressed for invisible operation

## Usage

### For Students

Just compile your code normally:
```bash
./gradlew compileJava
# or
gradle build
```

The telemetry system runs transparently in the background.

### For Administrators

1. Set up the central logging repository (e.g., `https://github.com/Arnav92/cheat_logging.git`)
2. Students need git credentials configured for push access
3. Monitor `{username}.jsonl` files for suspicious patterns

### Telemetry Data Format

Each line in `telemetry.jsonl` contains:
```json
{
  "timestamp": "2026-02-11T00:12:32.869019Z",
  "user": "student_username",
  "chars_added": 13710,
  "time_delta": 1.0,
  "velocity": 13710.0,
  "is_suspicious": true
}
```

## Example Scenarios

### Scenario 1: Normal Typing
Student types code gradually:
- 50 characters added in 30 seconds
- Velocity: 1.67 chars/sec
- `is_suspicious: false`

### Scenario 2: Code Paste (Cheating)
Student pastes a 200-line solution:
- 5,000 characters added in 2 seconds
- Velocity: 2,500 chars/sec
- `is_suspicious: true` ✓ Detected!

## Files

- `sentinel.py` - Activity tracking script
- `sync.py` - Background sync script
- `build.gradle` - Gradle build configuration
- `src/main/java/Solution.java` - Example solution file (for testing)
- `.sentinel_state.json` - Hidden state file (gitignored)
- `telemetry.jsonl` - Local telemetry log (gitignored)

## Requirements

- Python 3.6+
- Gradle 6.0+
- Java 11+
- Git credentials configured for push access to logging repository

## Security & Privacy

- All operations are silent and non-intrusive
- Build never fails due to telemetry errors
- Local files are gitignored to prevent accidental commits
- Telemetry data contains only: timestamp, username, character counts, and velocity

## Testing

The system has been tested with:
- ✓ Large code pastes (13,710+ chars) - correctly flagged as suspicious
- ✓ Normal incremental edits (1-2 chars/sec) - not flagged
- ✓ Build resilience - always succeeds even on errors
- ✓ Background sync - non-blocking using subprocess.Popen