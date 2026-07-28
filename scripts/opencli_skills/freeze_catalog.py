#!/usr/bin/env python3
"""Freeze an installed OpenCLI raw manifest into a deterministic repository input."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from scripts.opencli_skills.generate import OPENCLI_VERSION


def freeze_catalog(
    source: Path,
    destination: Path,
    *,
    expected_source_sha256: str,
) -> None:
    raw_bytes = source.read_bytes()
    source_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    if source_sha256 != expected_source_sha256.lower():
        raise ValueError(
            "OpenCLI raw manifest fingerprint changed: "
            f"{source_sha256} != {expected_source_sha256.lower()}"
        )
    raw_commands = json.loads(raw_bytes.decode("utf-8"))
    if not isinstance(raw_commands, list):
        raise ValueError("OpenCLI raw manifest must be a JSON array")
    commands = sorted(
        (dict(command) for command in raw_commands),
        key=lambda command: (str(command["site"]), str(command["name"])),
    )
    canonical = json.dumps(
        commands,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    snapshot = {
        "schema_version": 1,
        "opencli_version": OPENCLI_VERSION,
        "source": "cli-manifest.json",
        "source_sha256": source_sha256,
        "canonical_sha256": hashlib.sha256(canonical).hexdigest(),
        "commands": commands,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--expected-source-sha256", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    freeze_catalog(
        args.source,
        args.destination,
        expected_source_sha256=args.expected_source_sha256,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
