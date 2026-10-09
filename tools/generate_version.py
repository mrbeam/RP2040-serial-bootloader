#!/usr/bin/env python3
"""Generate a C version header from the bootloader's own Git checkout."""
import argparse
from pathlib import Path
import re
import subprocess

VERSION_PATTERN = re.compile(
    r"v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?P<alpha>a\d+)?(?P<metadata>[-+][A-Za-z0-9.+-]+)?"
)
DESCRIPTION_PATTERN = re.compile(
    r"(?P<tag>.+)-(?P<distance>\d+)-g(?P<revision>[0-9a-f]+)(?P<dirty>-dirty)?"
)


def git(source, *arguments):
    result = subprocess.run(
        ["git", "-C", str(source), *arguments],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def git_version(source):
    # Do not inherit the application repository's version from a source archive.
    if Path(git(source, "rev-parse", "--show-toplevel")).resolve() != source.resolve():
        raise ValueError("Bootloader Git metadata is missing; use --version-override")
    try:
        description = git(source, "describe", "--tags", "--match", "v[0-9]*",
                          "--long", "--abbrev=7", "--dirty")
    except subprocess.CalledProcessError:
        revision = git(source, "rev-parse", "--short=7", "HEAD")
        status = subprocess.run(["git", "-C", str(source), "diff-index", "--quiet", "HEAD", "--"])
        if status.returncode not in (0, 1):
            raise ValueError("Unable to determine bootloader working-tree state")
        return f"v0.0.0+0.g{revision}" + (".dirty" if status.returncode else "")

    match = DESCRIPTION_PATTERN.fullmatch(description)
    if not match:
        raise ValueError(f"Unexpected Git description: {description}")
    tag, distance, revision, dirty = match.group("tag", "distance", "revision", "dirty")
    version = tag
    if distance != "0" or dirty:
        version += f"+{distance}.g{revision}"
    if dirty:
        version += ".dirty"
    return version


def version_header(version):
    match = VERSION_PATTERN.fullmatch(version)
    if not match:
        raise ValueError(f"Invalid bootloader version: {version!r}; expected vMAJOR.MINOR.PATCH with optional alpha/metadata")
    values = {
        "MAJOR": match["major"],
        "MINOR": match["minor"],
        "PATCH": match["patch"],
        "OTHERS": (match["alpha"] or "") + (match["metadata"] or ""),
    }
    lines = ["#ifndef BL_VERSION_GENERATED_H_INCLUDED",
             "#define BL_VERSION_GENERATED_H_INCLUDED"]
    lines += [f'#define BL_VERSION_{name} "{value}"' for name, value in values.items()]
    lines += [f'#define BL_VERSION "{version}"', "#endif", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version-override", default="")
    args = parser.parse_args()
    try:
        version = args.version_override or git_version(args.source_dir)
        header = version_header(version)
        # Leave the timestamp untouched when the version is unchanged.
        if not args.output.exists() or args.output.read_text() != header:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(header)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Bootloader version error: {error}. Set BOOTLOADER_VERSION_OVERRIDE for source archives.\n")


if __name__ == "__main__":
    main()
