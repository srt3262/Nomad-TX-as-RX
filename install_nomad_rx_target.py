#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Install/update the RadioMaster Nomad-as-RX custom target for ExpressLRS v4.0.0+.

The reproducible baseline for this package is ExpressLRS 4.1.0.

Examples:
  python3 install_nomad_rx_target.py ~/elrs/ExpressLRS
  python3 install_nomad_rx_target.py ~/elrs/ExpressLRS/src
  python3 install_nomad_rx_target.py ~/elrs/ExpressLRS/src/hardware
  python3 install_nomad_rx_target.py ~/elrs/ExpressLRS --dry-run

This script modifies the ExpressLRS hardware registry:
  src/hardware/targets.json
  src/hardware/RX/Radiomaster Nomad RX FCC.json

It creates a timestamped backup of targets.json before writing unless --no-backup is used.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

MANUFACTURER = "radiomaster"
CATEGORY = "rx_dual"
TARGET_KEY = "nomad-rx-fcc"
LAYOUT_NAME = "Radiomaster Nomad RX FCC.json"
MIN_VERSION = "4.0.0"


def looks_like_hardware_dir(path: Path) -> bool:
    return (path / "targets.json").is_file() and (path / "RX").is_dir() and (path / "TX").is_dir()


def find_hardware_dir(start: Path) -> Path:
    candidates = [
        start,
        start / "hardware",
        start / "src" / "hardware",
        start / "ExpressLRS" / "src" / "hardware",
    ]
    for candidate in candidates:
        if looks_like_hardware_dir(candidate):
            return candidate.resolve()
    raise SystemExit(
        "Could not find the ExpressLRS hardware directory. Pass the directory that contains targets.json, RX/, and TX/. "
        "For ExpressLRS 4.1.0, clone https://github.com/ExpressLRS/Targets.git into ExpressLRS/src/hardware first."
    )


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def find_matching_brace(text: str, opening: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    raise SystemExit("Could not locate the closing brace in targets.json")


def find_keyed_object(
    text: str,
    key: str,
    start: int = 0,
    end: Optional[int] = None,
) -> tuple[re.Match[str], int, int]:
    pattern = re.compile(
        rf'^(?P<indent>[ \t]*)"{re.escape(key)}"\s*:\s*(?P<brace>\{{)',
        re.MULTILINE,
    )
    match = pattern.search(text, start, len(text) if end is None else end)
    if match is None:
        raise SystemExit(f'Could not locate object key "{key}" in targets.json')
    opening = match.start("brace")
    return match, opening, find_matching_brace(text, opening)


def render_object(value: dict[str, Any], key_indent: str) -> str:
    lines = json.dumps(value, indent=4, ensure_ascii=False).splitlines()
    return lines[0] + "".join(f"\n{key_indent}{line}" for line in lines[1:])


def upsert_target_text(text: str, entry: dict[str, Any]) -> str:
    _, manufacturer_open, manufacturer_close = find_keyed_object(text, MANUFACTURER)
    category_match, category_open, category_close = find_keyed_object(
        text,
        CATEGORY,
        manufacturer_open + 1,
        manufacturer_close,
    )

    try:
        target_match, target_open, target_close = find_keyed_object(
            text,
            TARGET_KEY,
            category_open + 1,
            category_close,
        )
    except SystemExit:
        target_match = None

    if target_match is not None:
        rendered = render_object(entry, target_match.group("indent"))
        return text[:target_open] + rendered + text[target_close + 1 :]

    category_indent = category_match.group("indent")
    target_indent = category_indent + "    "
    target_line = f'{target_indent}"{TARGET_KEY}": {render_object(entry, target_indent)}'

    closing_line_start = text.rfind("\n", category_open + 1, category_close) + 1
    if text[closing_line_start:category_close].strip():
        closing_line_start = category_close
    body = text[category_open + 1 : closing_line_start]

    if body.strip():
        last_content = closing_line_start - 1
        while last_content > category_open and text[last_content].isspace():
            last_content -= 1
        return (
            text[: last_content + 1]
            + ","
            + text[last_content + 1 : closing_line_start]
            + target_line
            + "\n"
            + category_indent
            + text[category_close:]
        )

    return text[:closing_line_start] + target_line + "\n" + category_indent + text[category_close:]


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def validate_layout(layout: dict[str, Any]) -> None:
    if layout.get("misc_fan_en") != 2:
        raise SystemExit("RX layout validation failed: expected misc_fan_en: 2")
    for required in ["radio_busy", "radio_dio1", "radio_nss", "radio_busy_2", "radio_dio1_2", "radio_nss_2"]:
        if required not in layout:
            raise SystemExit(f"RX layout validation failed: missing {required}")
    if layout.get("serial_rx") != 3 or layout.get("serial_tx") != 1:
        raise SystemExit("RX layout validation failed: expected full-duplex UART on GPIO3 RX / GPIO1 TX")
    if "radio_rfsw_ctrl" in layout:
        raise SystemExit("RX layout validation failed: obsolete radio_rfsw_ctrl override must be absent")
    if layout.get("power_apc2") != 26:
        raise SystemExit("RX layout validation failed: expected power_apc2: 26")
    if layout.get("power_control") != 3:
        raise SystemExit("RX layout validation failed: expected power_control: 3")
    if layout.get("power_values") != [120, 120, 120, 120, 120, 120, 95]:
        raise SystemExit("RX layout validation failed: unexpected official Nomad power_values table")


def validate_entry(entry: dict[str, Any]) -> None:
    if entry.get("firmware") != "Unified_ESP32_LR1121_RX":
        raise SystemExit("Target entry validation failed: firmware must be Unified_ESP32_LR1121_RX")
    if entry.get("layout_file") != LAYOUT_NAME:
        raise SystemExit(f"Target entry validation failed: layout_file must be {LAYOUT_NAME}")
    if entry.get("min_version") != MIN_VERSION:
        raise SystemExit(f"Target entry validation failed: min_version must be {MIN_VERSION}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the RadioMaster Nomad RX FCC target into an ExpressLRS v4 tree.")
    parser.add_argument("path", nargs="?", default=".", help="ExpressLRS repo root, src directory, or src/hardware directory")
    parser.add_argument("--dry-run", action="store_true", help="validate and print actions without writing files")
    parser.add_argument("--no-backup", action="store_true", help="do not create a targets.json backup")
    args = parser.parse_args()

    root = package_dir()
    layout_src = root / "RX" / LAYOUT_NAME
    entry_src = root / "targets-radiomaster-rx_dual-entry.json"
    if not layout_src.is_file():
        raise SystemExit(f"Missing package file: {layout_src}")
    if not entry_src.is_file():
        raise SystemExit(f"Missing package file: {entry_src}")

    layout = load_json(layout_src)
    target_blob = load_json(entry_src)
    if TARGET_KEY not in target_blob:
        raise SystemExit(f"Target entry file must contain key {TARGET_KEY}")
    entry = target_blob[TARGET_KEY]
    validate_layout(layout)
    validate_entry(entry)

    hardware_dir = find_hardware_dir(Path(args.path).expanduser().resolve())
    targets_json = hardware_dir / "targets.json"
    layout_dst = hardware_dir / "RX" / LAYOUT_NAME

    original_targets_text = targets_json.read_text(encoding="utf-8")
    data = load_json(targets_json)
    radiomaster = data.setdefault(MANUFACTURER, {"name": "Radiomaster"})
    radiomaster.setdefault("name", "Radiomaster")
    category = radiomaster.setdefault(CATEGORY, {})
    action = "update" if TARGET_KEY in category else "add"

    print(f"ExpressLRS hardware dir: {hardware_dir}")
    print(f"Will write layout:       {layout_dst}")
    print(f"Will {action} target:    {MANUFACTURER}.{CATEGORY}.{TARGET_KEY}")

    if args.dry_run:
        print("Dry run complete; no files were modified.")
        return 0

    if not args.no_backup:
        timestamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = targets_json.with_name(f"targets.json.bak-nomad-rx-{timestamp}")
        shutil.copy2(targets_json, backup)
        print(f"Backed up targets.json:  {backup}")

    layout_dst.write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8")
    category[TARGET_KEY] = entry
    targets_json.write_text(upsert_target_text(original_targets_text, entry), encoding="utf-8")

    # Read back exactly what was written.
    written_layout = load_json(layout_dst)
    written_targets = load_json(targets_json)
    written_entry = written_targets[MANUFACTURER][CATEGORY][TARGET_KEY]
    validate_layout(written_layout)
    validate_entry(written_entry)

    print("Installed and verified Nomad RX FCC target.")
    print("Build selector path: Radiomaster -> rx_dual -> RadioMaster Nomad RX FCC")
    return 0


if __name__ == "__main__":
    sys.exit(main())
