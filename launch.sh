#!/usr/bin/env bash
# SAP Interview Prep — Launch Script for macOS
# ─────────────────────────────────────────────
# Usage:
#   ./launch.sh              → Launch interactive study tool
#   ./launch.sh pdf          → (Re)generate all 3 PDF study guides
#   ./launch.sh help         → Show this help

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find Python 3 (prefer python3.13 from Homebrew on macOS)
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3.9 python3.8 python3; do
    if command -v "$candidate" &>/dev/null; then
        VER=$("$candidate" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo "$VER" | cut -d. -f1)
        MINOR=$(echo "$VER" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌  Python 3.8+ not found. Please install via: brew install python3"
    exit 1
fi

case "${1:-tool}" in
    pdf)
        echo "📄  Generating SAP Interview Prep PDFs..."
        echo "    Using: $PYTHON"
        "$PYTHON" "$SCRIPT_DIR/generate_pdfs.py"
        echo ""
        echo "✅  PDFs saved to: $SCRIPT_DIR/pdfs/"
        ls -lh "$SCRIPT_DIR/pdfs/"
        ;;
    help|-h|--help)
        echo ""
        echo "SAP Interview Prep — Launch Script"
        echo "──────────────────────────────────"
        echo "  ./launch.sh        → Launch interactive study tool"
        echo "  ./launch.sh pdf    → (Re)generate all 3 PDF guides"
        echo "  ./launch.sh help   → This help message"
        echo ""
        echo "PDFs are in: $SCRIPT_DIR/pdfs/"
        echo "Study guides: $SCRIPT_DIR/study_guides/"
        echo "Interactive tool: $SCRIPT_DIR/interactive_tool/main.py"
        echo ""
        ;;
    tool|*)
        cd "$SCRIPT_DIR/interactive_tool"
        "$PYTHON" main.py
        ;;
esac
