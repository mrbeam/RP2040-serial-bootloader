#!/usr/bin/env python3
"""Publish a bootloader UF2 under the version compiled into its header."""
import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--header", type=Path, required=True)
    parser.add_argument("--uf2", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    match = re.search(r'^#define BL_VERSION "(v[0-9A-Za-z.+-]+)"$',
                      args.header.read_text(), re.MULTILINE)
    if not match:
        parser.error("Compiled bootloader version is missing or invalid")
    output = args.output_dir / f"bootloader-{match[1]}.uf2"
    content = args.uf2.read_bytes()
    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists() or output.read_bytes() != content:
        output.write_bytes(content)
    print(output.name)


if __name__ == "__main__":
    main()
