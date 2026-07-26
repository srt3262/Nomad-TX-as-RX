# Build verification

The corrected target was compiled successfully on 2026-07-26 using:

- ExpressLRS `4.1.0`
- ExpressLRS commit `a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6`
- ExpressLRS Targets commit `7d7f15d832c3f6ddcf9c5148078075df03b0fd0a`
- PlatformIO environment `Unified_ESP32_LR1121_RX_via_UART`
- Target `radiomaster.rx_dual.nomad-rx-fcc`
- Regulatory domain `Regulatory_Domain_FCC_915`
- No private binding phrase or Wi-Fi credentials

Build result:

```text
Environment                         Status
Unified_ESP32_LR1121_RX_via_UART    SUCCESS
```

Resource use:

```text
RAM:   68,748 / 327,680 bytes (21.0%)
Flash: 1,249,809 / 1,966,080 bytes (63.6%)
```

The configured application image was 1,259,088 bytes with SHA-256:

```text
05b70fe925e1ef11b04eb42e6ee2dcbb5548cd342a04cdf635b30a668ab21e58
```

The embedded product name was `RadioMaster Nomad RX FCC`. The embedded hardware JSON contained GPIO3/GPIO1 full-duplex UART, both LR1121 radios, `power_apc2: 26`, `power_control: 3`, the official `95` calibration endpoint, and `misc_fan_en: 2`; it did not contain the older custom `radio_rfsw_ctrl` entry.

The hash above records the verification build; the binary is not included in the source package.
