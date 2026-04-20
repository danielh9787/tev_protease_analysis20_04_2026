#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID_ROWS = tuple("ABCDEFGH")


def load_condition_by_row(config_path: str | Path) -> dict[str, str]:
    payload = json.loads(Path(config_path).read_text(encoding="utf-8"))
    mapping = payload.get("condition_by_row")
    if not isinstance(mapping, dict):
        raise ValueError("config must include a condition_by_row mapping")

    missing_rows = [row for row in VALID_ROWS if row not in mapping]
    if missing_rows:
        raise ValueError(f"missing row mappings: {', '.join(missing_rows)}")

    return {row: str(mapping[row]) for row in VALID_ROWS}


def condition_for_well(well: str, condition_by_row: dict[str, str]) -> str:
    if not well:
        raise ValueError("well cannot be empty")
    row = well[0].upper()
    if row not in condition_by_row:
        raise ValueError(f"unsupported row '{row}' in well '{well}'")
    return condition_by_row[row]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Map plate wells to conditions by row")
    parser.add_argument("--config", required=True, help="Path to plate config (.yaml)")
    parser.add_argument("wells", nargs="+", help="Well IDs (e.g. A1 B1 H12)")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    mapping = load_condition_by_row(args.config)
    for well in args.wells:
        print(f"{well}\t{condition_for_well(well, mapping)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
