#!/usr/bin/env python3
"""Guarded BluOS volume-step harness command."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.bluos_readonly import fetch_endpoint, summarize


def parse_decimal(value: str, name: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"{name} must be a decimal number") from exc


def planned_db_after(current_db: Decimal, step_db: Decimal) -> Decimal:
    return current_db + step_db


def assert_safe_step(current_db: Decimal, step_db: Decimal, max_db: Decimal) -> Decimal:
    after_db = planned_db_after(current_db, step_db)
    if step_db > 0 and after_db > max_db:
        raise SystemExit(
            f"Refusing volume increase: current {current_db} dB + {step_db} dB "
            f"would exceed max {max_db} dB."
        )
    return after_db


def send_volume_step(host: str, port: int, step_db: Decimal, timeout: float) -> dict[str, Any]:
    query = urllib.parse.urlencode({"db": str(step_db)})
    url = f"http://{host}:{port}/Volume?{query}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            from scripts.bluos_readonly import parse_bluos_xml

            return summarize(parse_bluos_xml("Volume", response.read()))
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not send guarded BluOS volume step {url}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guarded BluOS volume step.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=11000)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--step-db", required=True, help="Signed dB delta, e.g. -1 or 1.")
    parser.add_argument("--max-db", required=True, help="Maximum allowed post-step dB, e.g. -24.")
    parser.add_argument(
        "--i-understand-this-changes-volume",
        action="store_true",
        help="Required acknowledgement because this changes amplifier volume.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.i_understand_this_changes_volume:
        raise SystemExit("Refusing to change volume without explicit acknowledgement flag.")

    step_db = parse_decimal(args.step_db, "step-db")
    max_db = parse_decimal(args.max_db, "max-db")
    before = summarize(fetch_endpoint(args.host, args.port, "volume", args.timeout))
    current_db = parse_decimal(str(before["db"]), "current db")
    planned_after = assert_safe_step(current_db, step_db, max_db)
    command_response = send_volume_step(args.host, args.port, step_db, args.timeout)
    after = summarize(fetch_endpoint(args.host, args.port, "volume", args.timeout))
    print(
        json.dumps(
            {
                "ok": True,
                "step_db": str(step_db),
                "max_db": str(max_db),
                "before": before,
                "planned_after_db": str(planned_after),
                "command_response": command_response,
                "after": after,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
