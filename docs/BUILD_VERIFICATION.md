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

The configured application image is included as:

```text
firmware/Nomad_RX_UART0_ELRS_4.1.0_FCC915_WIFI.bin
```

A merged ESP32 factory image is included as:

```text
firmware/Nomad_RX_UART0_ELRS_4.1.0_FCC915_FACTORY.bin
```

Its SHA-256 is:

```text
5e687f96efa18009565deebafc03ead7550d0a51fd3a4264c20c0247191c3c4e
```

The merged image was verified byte-for-byte against the build outputs at the standard ESP32 offsets: bootloader `0x1000`, partition table `0x8000`, boot-app image `0xE000`, and application `0x10000`. The application also passed the ESP32 checksum and validation-hash inspection.

This exact corrected rebuild still needs a physical reflash confirmation. The earlier UART0 build is the image used for the successful Nomad conversion and July 2026 hardware observations.
