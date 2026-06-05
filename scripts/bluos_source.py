#!/usr/bin/env python3
"""Guarded BluOS source discovery and switching harness."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.bluos_readonly import fetch_endpoint, summarize


@dataclass(frozen=True)
class BluosSource:
    text: str
    source_id: str | None
    url: str
    input_type: str | None
    service_type: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "id": self.source_id,
            "url": self.url,
            "input_type": self.input_type,
            "service_type": self.service_type,
        }


def parse_sources(xml_bytes: bytes) -> list[BluosSource]:
    root = ET.fromstring(xml_bytes)
    sources: list[BluosSource] = []
    for item in root.findall(".//item"):
        text = item.attrib.get("text")
        url = item.attrib.get("URL")
        if not text or not url:
            continue
        sources.append(
            BluosSource(
                text=text,
                source_id=item.attrib.get("id"),
                url=url,
                input_type=item.attrib.get("inputType"),
                service_type=item.attrib.get("serviceType"),
            )
        )
    return sources


def fetch_sources(host: str, port: int, timeout: float) -> list[BluosSource]:
    url = f"http://{host}:{port}/RadioBrowse?service=Capture"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return parse_sources(response.read())
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not fetch BluOS sources {url}: {exc}") from exc
    except ET.ParseError as exc:
        raise SystemExit(f"BluOS sources endpoint returned invalid XML: {exc}") from exc


def find_source(sources: list[BluosSource], text: str) -> BluosSource:
    matches = [source for source in sources if source.text.casefold() == text.casefold()]
    if not matches:
        available = ", ".join(source.text for source in sources)
        raise SystemExit(f"Source {text!r} not found. Available: {available}")
    if len(matches) > 1:
        raise SystemExit(f"Source {text!r} is ambiguous.")
    return matches[0]


def play_url_parameter(source_url: str) -> str:
    return urllib.parse.quote(urllib.parse.unquote(source_url), safe="")


def send_source_switch(host: str, port: int, source: BluosSource, timeout: float) -> dict[str, Any]:
    encoded_url = play_url_parameter(source.url)
    url = f"http://{host}:{port}/Play?url={encoded_url}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not switch BluOS source with {url}: {exc}") from exc
    try:
        root = ET.fromstring(body)
        return {
            "root": root.tag,
            "text": (root.text or "").strip(),
            "attributes": dict(root.attrib),
        }
    except ET.ParseError:
        return {"raw": body.decode(errors="replace")}


def send_input_type_index_switch(
    host: str, port: int, input_type_index: str, timeout: float
) -> dict[str, Any]:
    query = urllib.parse.urlencode({"inputTypeIndex": input_type_index})
    url = f"http://{host}:{port}/Play?{query}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not switch BluOS source with {url}: {exc}") from exc
    try:
        root = ET.fromstring(body)
        return {
            "root": root.tag,
            "text": (root.text or "").strip(),
            "attributes": dict(root.attrib),
        }
    except ET.ParseError:
        return {"raw": body.decode(errors="replace")}


def safe_abs_db_value(value: str) -> str:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("safe-db must be a decimal dB value") from exc
    if parsed > Decimal("-24"):
        raise argparse.ArgumentTypeError("safe-db must not exceed -24 dB")
    return str(parsed)


def send_safe_abs_db(host: str, port: int, safe_db: str, timeout: float) -> dict[str, Any]:
    query = urllib.parse.urlencode({"abs_db": safe_db})
    url = f"http://{host}:{port}/Volume?{query}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not set safe BluOS source volume with {url}: {exc}") from exc
    try:
        root = ET.fromstring(body)
        return {
            "root": root.tag,
            "text": (root.text or "").strip(),
            "attributes": dict(root.attrib),
        }
    except ET.ParseError:
        return {"raw": body.decode(errors="replace")}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BluOS source discovery and guarded switching.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=11000)
    parser.add_argument("--timeout", type=float, default=5.0)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    switch_parser = subparsers.add_parser("switch")
    switch_parser.add_argument("--source", required=True)
    switch_parser.add_argument(
        "--safe-db",
        type=safe_abs_db_value,
        help="Optional absolute dB target to set after source switch, capped at -24 dB.",
    )
    switch_parser.add_argument(
        "--input-type-index",
        help="Use /Play?inputTypeIndex=... instead of /Play?url=... for this source.",
    )
    switch_parser.add_argument(
        "--i-understand-this-changes-source",
        action="store_true",
        help="Required acknowledgement because this changes amplifier source.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sources = fetch_sources(args.host, args.port, args.timeout)
    if args.command == "list":
        print(json.dumps([source.to_dict() for source in sources], sort_keys=True))
        return 0

    if not args.i_understand_this_changes_source:
        raise SystemExit("Refusing to change source without explicit acknowledgement flag.")

    source = find_source(sources, args.source)
    before = summarize(fetch_endpoint(args.host, args.port, "status", args.timeout))
    if args.input_type_index:
        command_response = send_input_type_index_switch(
            args.host, args.port, args.input_type_index, args.timeout
        )
        switch_method = {"kind": "inputTypeIndex", "value": args.input_type_index}
    else:
        command_response = send_source_switch(args.host, args.port, source, args.timeout)
        switch_method = {"kind": "url", "value": play_url_parameter(source.url)}
    safe_volume_response = None
    if args.safe_db is not None:
        safe_volume_response = send_safe_abs_db(args.host, args.port, args.safe_db, args.timeout)
    after = summarize(fetch_endpoint(args.host, args.port, "status", args.timeout))
    print(
        json.dumps(
            {
                "ok": True,
                "requested_source": source.to_dict(),
                "switch_method": switch_method,
                "safe_db": args.safe_db,
                "safe_volume_response": safe_volume_response,
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
