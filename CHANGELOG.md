# Changelog

## 0.2.0 - 2026-07-26

- Pinned the reproducible baseline to ExpressLRS 4.1.0 commit `a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6` and target database commit `7d7f15d832c3f6ddcf9c5148078075df03b0fd0a`.
- Removed the obsolete custom `radio_rfsw_ctrl` override.
- Restored the official Nomad GPIO26 APC2 path with `power_apc2: 26` and `power_control: 3`.
- Restored the official calibrated `power_values` endpoint of `95`.
- Retained both LR1121 radios, GPIO3/GPIO1 full-duplex UART, and GPIO2 fan enable.
- Hardened the installer and verifier against regression to the older layout.
- Changed target installation to preserve the official registry's formatting and produce a minimal 13-line registry diff.
- Added automated tests, GitHub Actions validation, upstream attribution, contribution guidance, and GPL-3.0-or-later licensing.
- Verified a full `Unified_ESP32_LR1121_RX_via_UART` build with the corrected target on ExpressLRS 4.1.0.
- Documented the July 2026 test observations and remaining validation work.

## 2026-06-25

- Added git-friendly ELRS v4.0.0+ RadioMaster Nomad-as-RX target package.
- Added custom target entry `radiomaster.rx_dual.nomad-rx-fcc`.
- Added RX hardware layout with `misc_fan_en: 2`.
- Added install and verify scripts.
- Added WebUI hardware-layout fallback JSON.
- Added optional force-fan validation snippet.
