# Project notice

This is an unofficial community project for running a RadioMaster Nomad Gemini Xrossband transmitter module as an ExpressLRS receiver. It is not affiliated with, endorsed by, or supported by RadioMaster or the ExpressLRS project.

The target is derived from the official RadioMaster Nomad hardware definition and is intended to be built with the GPL-licensed ExpressLRS source. The validated upstream baseline is:

- ExpressLRS release: `4.1.0`
- ExpressLRS commit: `a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6`
- Official target repository: `ExpressLRS/Targets`
- Target database commit: `7d7f15d832c3f6ddcf9c5148078075df03b0fd0a`
- Official Nomad definition: `TX/Radiomaster Nomad.json`

The conversion-specific changes are:

- Use receiver firmware: `Unified_ESP32_LR1121_RX`
- Use full-duplex UART on GPIO3 RX and GPIO1 TX
- Remove transmitter backpack controls
- Retain both LR1121 radios, official GPIO26 APC2 power control, calibrated power tables, RGB LEDs, buttons, and GPIO2 fan enable

RadioMaster and ExpressLRS names are used only to identify compatibility. All trademarks belong to their respective owners.

The software and hardware information are provided without warranty. Keep a recovery image and understand the bootloader/flash recovery procedure before modifying hardware.
