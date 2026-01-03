#!/bin/bash
# Auto-sync GEMINI.md with claude-cognitive attention state
# Run this periodically (e.g., cron every 5 minutes) or after major work sessions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Generate fresh GEMINI.md
cd "$PROJECT_ROOT"
python3 "$SCRIPT_DIR/generate-gemini-md.py"

echo "✅ GEMINI.md synchronized with claude-cognitive state"
echo "💡 Gemini CLI will now have up-to-date context"
