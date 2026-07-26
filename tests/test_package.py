# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_PATH = ROOT / "RX" / "Radiomaster Nomad RX FCC.json"
UPLOAD_LAYOUT_PATH = ROOT / "hardware-upload" / "hardware-nomad-rx-fcc-v4-fan.json"
ENTRY_PATH = ROOT / "targets-radiomaster-rx_dual-entry.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PackageTests(unittest.TestCase):
    def test_layout_uses_corrected_nomad_power_path(self) -> None:
        layout = load_json(LAYOUT_PATH)
        self.assertIsInstance(layout, dict)
        assert isinstance(layout, dict)

        self.assertEqual(layout["serial_rx"], 3)
        self.assertEqual(layout["serial_tx"], 1)
        self.assertEqual(layout["power_apc2"], 26)
        self.assertEqual(layout["power_control"], 3)
        self.assertEqual(layout["power_values"], [120, 120, 120, 120, 120, 120, 95])
        self.assertNotIn("radio_rfsw_ctrl", layout)

    def test_dual_radio_and_fan_pins_are_present(self) -> None:
        layout = load_json(LAYOUT_PATH)
        assert isinstance(layout, dict)

        for key in (
            "radio_busy",
            "radio_dio1",
            "radio_nss",
            "radio_rst",
            "radio_busy_2",
            "radio_dio1_2",
            "radio_nss_2",
            "radio_rst_2",
        ):
            self.assertIn(key, layout)
        self.assertEqual(layout["misc_fan_en"], 2)

    def test_webui_fallback_matches_source_layout(self) -> None:
        self.assertEqual(load_json(LAYOUT_PATH), load_json(UPLOAD_LAYOUT_PATH))

    def test_target_registry_entry(self) -> None:
        entry_blob = load_json(ENTRY_PATH)
        assert isinstance(entry_blob, dict)
        entry = entry_blob["nomad-rx-fcc"]

        self.assertEqual(entry["layout_file"], LAYOUT_PATH.name)
        self.assertEqual(entry["firmware"], "Unified_ESP32_LR1121_RX")
        self.assertEqual(entry["platform"], "esp32")

    def test_install_and_verify_against_synthetic_elrs_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            elrs_root = Path(tmp) / "ExpressLRS"
            hardware = elrs_root / "src" / "hardware"
            (hardware / "RX").mkdir(parents=True)
            (hardware / "TX").mkdir()
            (hardware / "targets.json").write_text(
                """{
    "radiomaster": {
        "name": "Radiomaster",
        "rx_dual": {
            "existing": {
                "product_name": "Existing",
                "upload_methods": ["uart", "wifi"]
            }
        },
        "tx_dual": {}
    },
    "sentinel": {"keep": [1, 2, 3]}
}
""",
                encoding="utf-8",
            )

            install = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "install_nomad_rx_target.py"),
                    str(elrs_root),
                    "--no-backup",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)

            installed_targets = (hardware / "targets.json").read_text(encoding="utf-8")
            self.assertIn('"upload_methods": ["uart", "wifi"]', installed_targets)
            self.assertIn('"sentinel": {"keep": [1, 2, 3]}', installed_targets)
            self.assertEqual(installed_targets.count('"nomad-rx-fcc"'), 1)

            reinstall = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "install_nomad_rx_target.py"),
                    str(elrs_root),
                    "--no-backup",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(reinstall.returncode, 0, reinstall.stdout + reinstall.stderr)
            self.assertEqual(installed_targets, (hardware / "targets.json").read_text(encoding="utf-8"))

            verify = subprocess.run(
                [sys.executable, str(ROOT / "verify_nomad_rx_target.py"), str(elrs_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
            self.assertIn("Verification passed.", verify.stdout)


if __name__ == "__main__":
    unittest.main()
