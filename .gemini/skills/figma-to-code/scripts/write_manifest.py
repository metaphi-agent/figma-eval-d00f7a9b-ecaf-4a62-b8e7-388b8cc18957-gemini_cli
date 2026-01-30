#!/usr/bin/env python3
"""
Write or update figma-to-code session manifest.

Usage:
    # Initialize after extraction
    python write_manifest.py <manifest_path> extracted <figma_file_key>

    # Update to building phase
    python write_manifest.py <manifest_path> building

    # Save preview URL (Modal sandbox)
    python write_manifest.py <manifest_path> preview <preview_url>

    # Complete with dist path
    python write_manifest.py <manifest_path> complete <dist_path>

Output:
    SUCCESS:<manifest_path>
    ERROR:<error_message>

Example:
    $ python write_manifest.py /work/123/figma-to-code/manifest.json extracted abc123
    SUCCESS:/work/123/figma-to-code/manifest.json
"""
import json
import os
import sys
from datetime import datetime, timezone


def load_manifest(path: str) -> dict:
    """Load existing manifest or return empty structure."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_manifest(path: str, manifest: dict) -> None:
    """Save manifest to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)


def main():
    if len(sys.argv) < 3:
        print("Usage: python write_manifest.py <manifest_path> <command> [args...]", file=sys.stderr)
        sys.exit(1)

    manifest_path = sys.argv[1]
    command = sys.argv[2]

    try:
        manifest = load_manifest(manifest_path)

        # Initialize session_id if new manifest
        if "session_id" not in manifest:
            manifest["session_id"] = f"figma_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
            manifest["created_at"] = datetime.now(timezone.utc).isoformat()

        manifest["updated_at"] = datetime.now(timezone.utc).isoformat()

        if command == "extracted":
            if len(sys.argv) != 4:
                print("Usage: python write_manifest.py <path> extracted <figma_file_key>", file=sys.stderr)
                sys.exit(1)
            manifest["phase"] = "extracted"
            manifest["figma_file_key"] = sys.argv[3]

        elif command == "building":
            manifest["phase"] = "building"

        elif command == "preview":
            if len(sys.argv) != 4:
                print("Usage: python write_manifest.py <path> preview <preview_url>", file=sys.stderr)
                sys.exit(1)
            manifest["preview_url"] = sys.argv[3]

        elif command == "complete":
            if len(sys.argv) != 4:
                print("Usage: python write_manifest.py <path> complete <dist_path>", file=sys.stderr)
                sys.exit(1)
            manifest["phase"] = "complete"
            manifest["dist_path"] = sys.argv[3]
            manifest["completed_at"] = datetime.now(timezone.utc).isoformat()

        else:
            print(f"ERROR:unknown_command:{command}")
            sys.exit(1)

        save_manifest(manifest_path, manifest)
        print(f"SUCCESS:{manifest_path}")

    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
