# RadioMaster Nomad TX as ExpressLRS RX

An unofficial, open-source target package for flashing a **RadioMaster Nomad Gemini Xrossband TX module as an ExpressLRS RX**.

The validated baseline is **ExpressLRS 4.1.0**, tag commit:

```text
a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6
```

The matching ExpressLRS target database baseline is:

```text
7d7f15d832c3f6ddcf9c5148078075df03b0fd0a
```

The target declares ELRS 4.0.0 as its minimum version, but 4.1.0 is the reproducible and tested source baseline for this master.

The custom target adds:

```text
Manufacturer: Radiomaster
Category:      rx_dual
Target key:    nomad-rx-fcc
Product name:  RadioMaster Nomad RX FCC
Firmware:      Unified_ESP32_LR1121_RX
Min version:   4.0.0
```

The important hardware addition is the Nomad fan-enable pin:

```json
"misc_fan_en": 2
```

The receiver UART is explicitly configured for two-wire full-duplex operation:

```text
GPIO3 = RX
GPIO1 = TX
```

The corrected master retains both LR1121 radios and the official Nomad GPIO26 APC2 power-control path and calibration tables. It removes the older custom `radio_rfsw_ctrl` override. See [`docs/MASTER_CORRECTIONS.md`](docs/MASTER_CORRECTIONS.md) for the exact differences.

On RX firmware, normal TX fan menu items such as `fan-mode` and `power-fan-threshold` are not expected to appear. Validate the active device `hardware.json` and actual GPIO2/fan behavior instead.

## Project status

- Source target, installer, verifier, tests, and WebUI fallback layout are included.
- The corrected target compiles successfully as `Unified_ESP32_LR1121_RX_via_UART` on ExpressLRS 4.1.0.
- The two-wire UART conversion has bound and operated as an ELRS receiver.
- A 12 V supply materially improved observed telemetry range compared with USB-C power in the July 2026 tests.
- Flight-controller CRSF/MAVLink interoperability, sustained high-power thermal behavior, and single-wire S.Port operation still need independent testing.
- This repository does not currently include a prebuilt firmware binary.

See [`docs/BUILD_VERIFICATION.md`](docs/BUILD_VERIFICATION.md) for the reproducible compile record and [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md) for hardware observations and remaining validation work.

---

## Package contents

```text
.
├── README.md
├── LICENSE
├── NOTICE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── VERSION
├── SHA256SUMS
├── install_nomad_rx_target.py
├── verify_nomad_rx_target.py
├── RX/
│   └── Radiomaster Nomad RX FCC.json
├── hardware-upload/
│   └── hardware-nomad-rx-fcc-v4-fan.json
├── targets-radiomaster-rx_dual-entry.json
├── examples/
│   └── super_defines.fcc915.example.txt
├── patches/
│   └── force_fan_on_snippet.txt
├── docs/
│   ├── BUILD_VERIFICATION.md
│   ├── MASTER_CORRECTIONS.md
│   └── TEST_RESULTS.md
└── tests/
    └── test_package.py
```

### File roles

| File | Purpose |
|---|---|
| `install_nomad_rx_target.py` | Installs/updates the custom target inside an ExpressLRS source tree. |
| `verify_nomad_rx_target.py` | Verifies the local source tree and optionally checks a flashed device over WebUI. |
| `RX/Radiomaster Nomad RX FCC.json` | The RX hardware layout with `misc_fan_en: 2`. |
| `hardware-upload/hardware-nomad-rx-fcc-v4-fan.json` | Same layout, named for manual upload through WebUI if needed. |
| `targets-radiomaster-rx_dual-entry.json` | Reference target-registry entry inserted into `src/hardware/targets.json`. |
| `examples/super_defines.fcc915.example.txt` | Example FCC 915 build defines. |
| `patches/force_fan_on_snippet.txt` | Optional emergency fallback if the fan pin is present but RX firmware never asserts it. |
| `tests/test_package.py` | Verifies corrected pin/power values and exercises install/verify behavior. |
| `SHA256SUMS` | Integrity hashes for every other file in the source package. |

---

## Safety and setup notes

- Use the correct regulatory domain for your location and hardware.
- Do not run high RF power without a proper antenna or dummy load.
- For 1 W telemetry testing, confirm fan operation before enclosing or deploying the module.
- Both ends of the ELRS link must use the same major version. This package is for ELRS v4.x.
- For first flash after converting from TX-module firmware to RX firmware, use UART/USB flashing and erase flash first.
- Keep a known-good recovery image before the first conversion flash.
- The informal test observations in this repository are not guaranteed range specifications.

---

## Ubuntu 24.04 workflow

### 1. Get ExpressLRS v4

```bash
mkdir -p ~/elrs
cd ~/elrs
git clone https://github.com/ExpressLRS/ExpressLRS.git
cd ExpressLRS
git fetch --tags
git checkout 4.1.0
git rev-parse HEAD
```

Expected commit:

```text
a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6
```

ExpressLRS loads its hardware registry from `src/hardware`. Populate it from the official target repository and pin the matching baseline:

```bash
git clone https://github.com/ExpressLRS/Targets.git src/hardware
git -C src/hardware checkout 7d7f15d832c3f6ddcf9c5148078075df03b0fd0a
```

Newer v4.x releases may work, but should be treated as unverified until the target is rebuilt and tested.

### 2. Install Python / PlatformIO tools

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip unzip build-essential

cd ~/elrs/ExpressLRS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install platformio dronecan setuptools empy==3.3.4 pexpect
```

### 3. Install this custom target

From wherever this folder lives:

```bash
python3 /path/to/nomad-tx-as-rx/install_nomad_rx_target.py ~/elrs/ExpressLRS
```

The script also accepts any of these paths:

```text
~/elrs/ExpressLRS
~/elrs/ExpressLRS/src
~/elrs/ExpressLRS/src/hardware
```

It modifies:

```text
~/elrs/ExpressLRS/src/hardware/targets.json
~/elrs/ExpressLRS/src/hardware/RX/Radiomaster Nomad RX FCC.json
```

It also creates a timestamped backup of `targets.json`.

### 4. Verify local source files

```bash
python3 /path/to/nomad-tx-as-rx/verify_nomad_rx_target.py ~/elrs/ExpressLRS
```

Expected final line:

```text
Verification passed.
```

You can also manually check:

```bash
grep -n "nomad-rx-fcc" ~/elrs/ExpressLRS/src/hardware/targets.json
grep -n "misc_fan_en" ~/elrs/ExpressLRS/src/hardware/RX/Radiomaster\ Nomad\ RX\ FCC.json
```

Expected fan result:

```json
"misc_fan_en": 2
```

### 5. Create build defines

```bash
cd ~/elrs/ExpressLRS/src
cp /path/to/nomad-tx-as-rx/examples/super_defines.fcc915.example.txt super_defines.txt
nano super_defines.txt
```

At minimum, set:

```text
-DRegulatory_Domain_FCC_915
-DMY_BINDING_PHRASE="ReplaceWithYourBindingPhrase"
```

Keep the binding phrase the same on the other ELRS device.

### 6. Build

```bash
cd ~/elrs/ExpressLRS/src
pio run -e Unified_ESP32_LR1121_RX_via_UART
```

When prompted to choose the firmware configuration, do **not** leave it bare. Select:

```text
Radiomaster -> rx_dual -> RadioMaster Nomad RX FCC
```

or the equivalent target key:

```text
radiomaster.rx_dual.nomad-rx-fcc
```

### 7. Flash over UART/USB

Find the port:

```bash
pio device list
```

Erase and flash, replacing `/dev/ttyUSB0` with the actual port:

```bash
cd ~/elrs/ExpressLRS/src
pio run -e Unified_ESP32_LR1121_RX_via_UART -t erase --upload-port /dev/ttyUSB0
pio run -e Unified_ESP32_LR1121_RX_via_UART -t upload --upload-port /dev/ttyUSB0
```

If upload fails, put the ESP32 into bootloader mode, then run the upload again.

---

## Windows workflow

PowerShell commands:

```powershell
mkdir C:\elrs
cd C:\elrs
git clone https://github.com/ExpressLRS/ExpressLRS.git
cd C:\elrs\ExpressLRS
git fetch --tags
git checkout 4.1.0
git rev-parse HEAD
git clone https://github.com/ExpressLRS/Targets.git src\hardware
git -C src\hardware checkout 7d7f15d832c3f6ddcf9c5148078075df03b0fd0a
```

Create and activate a Python environment:

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install platformio dronecan setuptools empy==3.3.4 pexpect
```

Install the target:

```powershell
py C:\path\to\nomad-tx-as-rx\install_nomad_rx_target.py C:\elrs\ExpressLRS
```

Verify:

```powershell
py C:\path\to\nomad-tx-as-rx\verify_nomad_rx_target.py C:\elrs\ExpressLRS
```

Create `super_defines.txt`:

```powershell
cd C:\elrs\ExpressLRS\src
Copy-Item C:\path\to\nomad-tx-as-rx\examples\super_defines.fcc915.example.txt .\super_defines.txt
notepad .\super_defines.txt
```

Build:

```powershell
cd C:\elrs\ExpressLRS\src
pio run -e Unified_ESP32_LR1121_RX_via_UART
```

Select:

```text
Radiomaster -> rx_dual -> RadioMaster Nomad RX FCC
```

Find the COM port:

```powershell
pio device list
```

Erase and flash, replacing `COM5` with the actual port:

```powershell
pio run -e Unified_ESP32_LR1121_RX_via_UART -t erase --upload-port COM5
pio run -e Unified_ESP32_LR1121_RX_via_UART -t upload --upload-port COM5
```

---

## Device verification after flashing

After flashing, power-cycle the Nomad. Connect to the RX WebUI by one of these methods:

```text
http://10.0.0.1/
http://elrs_rx.local/
```

Then check the active hardware JSON:

```text
http://10.0.0.1/hardware.json
```

or on Ubuntu:

```bash
curl http://10.0.0.1/hardware.json | grep -i fan
```

Expected:

```json
"misc_fan_en":2
```

Spacing may differ.

The verify script can also check the device:

```bash
python3 /path/to/nomad-tx-as-rx/verify_nomad_rx_target.py ~/elrs/ExpressLRS --device-url http://10.0.0.1
```

Expected:

```text
OK:   device hardware.json contains misc_fan_en: 2
Verification passed.
```

---

## If the flashed device is missing `misc_fan_en`

This usually means one of these happened:

1. The firmware was built as a bare image.
2. The wrong target was selected.
3. A stale hardware override is still active in flash.
4. The target was installed into the wrong ExpressLRS checkout.

First try a clean rebuild and erase/flash:

```bash
cd ~/elrs/ExpressLRS/src
pio run -e Unified_ESP32_LR1121_RX_via_UART -t clean
rm -rf .pio/build/Unified_ESP32_LR1121_RX_via_UART
pio run -e Unified_ESP32_LR1121_RX_via_UART
pio run -e Unified_ESP32_LR1121_RX_via_UART -t erase --upload-port /dev/ttyUSB0
pio run -e Unified_ESP32_LR1121_RX_via_UART -t upload --upload-port /dev/ttyUSB0
```

If the firmware name is correct but `hardware.json` still lacks the fan pin, use the manual WebUI fallback:

1. Open the RX WebUI.
2. Go to the hardware layout page.
3. Upload:

```text
hardware-upload/hardware-nomad-rx-fcc-v4-fan.json
```

4. Save/reboot.
5. Recheck:

```text
http://10.0.0.1/hardware.json
```

---

## Fan test checklist

Do not depend on a visible fan option in the RX WebUI. Test the actual hardware behavior.

1. Attach antennas or RF dummy loads.
2. Power the Nomad from a known-good supply.
3. Confirm the active `hardware.json` contains `misc_fan_en: 2`.
4. Connect/link to the other ELRS v4 device.
5. Increase RX telemetry power step by step.
6. Probe GPIO2 or the fan-enable net with a DMM or scope.
7. Confirm fan spin and module temperature stabilization.

Expected outcomes:

| Result | Meaning |
|---|---|
| `misc_fan_en` present and fan spins | Target and fan behavior are working. |
| `misc_fan_en` present, GPIO2 goes high, fan does not spin | Fan supply, MOSFET, connector, or mechanical fan issue. |
| `misc_fan_en` present, GPIO2 never changes | RX firmware path may not be invoking fan control. See the fallback snippet. |
| Fan always on | Acceptable for platform testing if current and thermal behavior are acceptable. |

---

## Optional force-fan fallback

Use this only if:

```text
active hardware.json contains "misc_fan_en": 2
GPIO2 never asserts during high telemetry-power testing
```

See:

```text
patches/force_fan_on_snippet.txt
```

The fallback concept is:

```cpp
#ifdef NOMAD_RX_FORCE_FAN
    pinMode(2, OUTPUT);
    digitalWrite(2, HIGH);
#endif
```

and add this to `src/super_defines.txt`:

```text
-DNOMAD_RX_FORCE_FAN
```

For a 1 W telemetry platform, fan always-on is safer than fan never-on.

---

## Reusing this package after an ELRS update

After pulling a newer ELRS v4 tag or replacing the ExpressLRS source tree, rerun:

```bash
python3 /path/to/nomad-tx-as-rx/install_nomad_rx_target.py ~/elrs/ExpressLRS
python3 /path/to/nomad-tx-as-rx/verify_nomad_rx_target.py ~/elrs/ExpressLRS
```

Then rebuild and flash the same way.

This keeps the custom target reproducible without relying on memory or manual JSON edits.

## Validate this repository

These checks require only Python 3.9 or newer:

```bash
python -m compileall -q install_nomad_rx_target.py verify_nomad_rx_target.py tests
python -m unittest discover -s tests -v
```

## License and upstream

This project is licensed under **GPL-3.0-or-later**. ExpressLRS is the upstream GPL-licensed firmware project; this repository supplies a conversion target and supporting tooling, not a replacement for ExpressLRS.

See [`NOTICE.md`](NOTICE.md) for upstream attribution and the exact baseline.
