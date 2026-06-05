#!/usr/bin/env python3
"""Guarded BluOS mute harness command."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.bluos_readonly import fetch_endpoint, parse_bluos_xml, summarize


def mute_value(state: str) -> str:
    if state == "on":
        return "1"
    if state == "off":
        return "0"
    raise ValueError(f"unsupported mute state: {state}")


def send_mute(host: str, port: int, state: str, timeout: float) -> dict[str, Any]:
    query = urllib.parse.urlencode({"mute": mute_value(state)})
    url = f"http://{host}:{port}/Volume?{query}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return summarize(parse_bluos_xml("Volume", response.read()))
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not send guarded BluOS mute command {url}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guarded BluOS mute command.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=11000)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--state", choices=["off", "on"], required=True)
    parser.add_argument(
        "--i-understand-this-changes-mute",
        action="store_true",
        help="Required acknowledgement because this changes amplifier mute state.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.i_understand_this_changes_mute:
        raise SystemExit("Refusing to change mute without explicit acknowledgement flag.")

    before = summarize(fetch_endpoint(args.host, args.port, "volume", args.timeout))
    command_response = send_mute(args.host, args.port, args.state, args.timeout)
    after = summarize(fetch_endpoint(args.host, args.port, "volume", args.timeout))
    print(
        json.dumps(
            {
                "ok": True,
                "requested_state": args.state,
                "requested_mute": mute_value(args.state),
                "before": before,
                "command_response": command_response,
                "after": after,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

