#!/usr/bin/env python3
"""
Check figma-to-code session state for resume capability.

Usage:
    python check_manifest.py <manifest_path>

Output:
    FRESH:no_manifest           - No existing session
    RESUME:extracted            - Figma extracted, can start coding
    RESUME:building             - In development, can resume
    COMPLETE:<dist_path>        - Build complete

Example:
    $ python check_manifest.py /work/123/figma-to-code/manifest.json
    RESUME:building
"""
import json
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_manifest.py <manifest_path>", file=sys.stderr)
        sys.exit(1)

    manifest_path = sys.argv[1]

    try:
        with open(manifest_path) as f:
            manifest = json.load(f)

        phase = manifest.get("phase", "")

        if phase == "complete":
            dist_path = manifest.get("dist_path", "")
            if dist_path:
                print(f"COMPLETE:{dist_path}")
            else:
                print("RESUME:building")
        elif phase == "building":
            print("RESUME:building")
        elif phase == "extracted":
            print("RESUME:extracted")
        elif phase == "init":
            print("FRESH:init_only")
        else:
            print("FRESH:unknown_phase")

    except FileNotFoundError:
        print("FRESH:no_manifest")
    except json.JSONDecodeError:
        print("FRESH:invalid_manifest")
    except Exception as e:
        print(f"FRESH:error:{str(e)}", file=sys.stderr)
        print("FRESH:error")


if __name__ == "__main__":
    main()
