#!/usr/bin/env python3
"""Read-only BluOS harness commands."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any

READ_ONLY_ENDPOINTS = {
    "status": "Status",
    "syncstatus": "SyncStatus",
    "volume": "Volume",
}


@dataclass(frozen=True)
class BluosResponse:
    endpoint: str
    root: str
    attributes: dict[str, str]
    text: str | None
    fields: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "root": self.root,
            "attributes": self.attributes,
            "text": self.text,
            "fields": self.fields,
        }


def parse_bluos_xml(endpoint: str, xml_bytes: bytes) -> BluosResponse:
    root = ET.fromstring(xml_bytes)
    fields: dict[str, str] = {}
    for child in root:
        text = (child.text or "").strip()
        if text:
            fields[child.tag] = text
    return BluosResponse(
        endpoint=endpoint,
        root=root.tag,
        attributes={key: value for key, value in root.attrib.items()},
        text=(root.text or "").strip() or None,
        fields=fields,
    )


def fetch_endpoint(host: str, port: int, command: str, timeout: float) -> BluosResponse:
    endpoint = READ_ONLY_ENDPOINTS[command]
    url = f"http://{host}:{port}/{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return parse_bluos_xml(endpoint, response.read())
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach BluOS endpoint {url}: {exc}") from exc
    except ET.ParseError as exc:
        raise SystemExit(f"BluOS endpoint {url} returned invalid XML: {exc}") from exc


def summarize(response: BluosResponse) -> dict[str, Any]:
    if response.root == "status":
        return {
            "endpoint": response.endpoint,
            "etag": response.attributes.get("etag"),
            "name": response.fields.get("name") or response.fields.get("title1"),
            "state": response.fields.get("state"),
            "service": response.fields.get("service"),
            "inputTypeIndex": response.fields.get("inputTypeIndex"),
            "volume": response.fields.get("volume"),
            "db": response.fields.get("db"),
            "mute": response.fields.get("mute"),
            "syncStat": response.fields.get("syncStat"),
        }
    if response.root == "SyncStatus":
        return {
            "endpoint": response.endpoint,
            "etag": response.attributes.get("etag"),
            "syncStat": response.attributes.get("syncStat"),
            "name": response.attributes.get("name"),
            "brand": response.attributes.get("brand"),
            "model": response.attributes.get("model"),
            "modelName": response.attributes.get("modelName"),
            "version": response.attributes.get("version"),
            "volume": response.attributes.get("volume"),
            "db": response.attributes.get("db"),
            "mute": response.attributes.get("mute"),
            "id": response.attributes.get("id"),
        }
    if response.root == "volume":
        return {
            "endpoint": response.endpoint,
            "volume": response.text,
            "db": response.attributes.get("db"),
            "mute": response.attributes.get("mute"),
            "etag": response.attributes.get("etag"),
            "offsetDb": response.attributes.get("offsetDb"),
        }
    return response.to_dict()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only BluOS harness.")
    parser.add_argument("--host", required=True, help="BluOS player host or IP.")
    parser.add_argument("--port", type=int, default=11000, help="BluOS player port.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds.")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print parsed raw XML structure instead of the safe summary.",
    )
    parser.add_argument("command", choices=["doctor", *READ_ONLY_ENDPOINTS])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = "syncstatus" if args.command == "doctor" else args.command
    response = fetch_endpoint(args.host, args.port, command, args.timeout)
    payload = response.to_dict() if args.raw else summarize(response)
    if args.command == "doctor":
        payload = {"ok": True, **payload}
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

