# Prebuilt RadioMaster Nomad RX firmware

These are the corrected ExpressLRS 4.1.0 FCC915 images for the supported two-wire UART conversion:

```text
GPIO3 = receiver RX
GPIO1 = receiver TX
```

No binding phrase or Wi-Fi credentials are compiled into either image. Configure those after flashing through the receiver WebUI.

## Which file to use

| File | Use |
|---|---|
| `Nomad_RX_UART0_ELRS_4.1.0_FCC915_WIFI.bin` | Upload through the ExpressLRS WebUI or the Configurator's local-firmware flow. This is the normal update image. |
| `Nomad_RX_UART0_ELRS_4.1.0_FCC915_FACTORY.bin` | Complete ESP32 image for serial/USB recovery or the initial conversion. Flash at address `0x0`; it contains the bootloader, partition table, boot-app image, and application. |
| `hardware.json` | Exact hardware definition embedded in the images. It can also be uploaded manually through the WebUI hardware-layout page if required. |

The first TX-to-RX conversion may be rejected by a product-type check. If the WebUI force-update path that was used for the original conversion is unavailable or fails, use the factory image through the ESP32 serial bootloader after making a recovery backup.

The factory image replaces the ESP32 flash layout and existing configuration. It is not the file to upload through the normal receiver WebUI.

## Build provenance

- Project release: `0.2.0`
- ExpressLRS: `4.1.0`
- ExpressLRS commit: `a9d4a9cb5b5687c4c9d7e9e7fbdf44ad93651da6`
- Targets commit: `7d7f15d832c3f6ddcf9c5148078075df03b0fd0a`
- Environment: `Unified_ESP32_LR1121_RX_via_UART`
- Target: `radiomaster.rx_dual.nomad-rx-fcc`
- Product: `RadioMaster Nomad RX FCC`
- Regulatory domain: `Regulatory_Domain_FCC_915`

The application image passed the ESP32 image checksum and validation-hash checks. Its embedded configuration was inspected for both LR1121 radios, GPIO26 APC2 power control, GPIO2 fan enable, GPIO3/GPIO1 UART, and the corrected power table.

The merged factory image was verified byte-for-byte at these offsets:

```text
0x001000  bootloader
0x008000  partition table
0x00E000  boot_app0
0x010000  application image
```

See `SHA256SUMS.txt` and `build-manifest.json` for exact hashes and sizes.

The experimental one-wire S.Port image from the earlier engineering bundle is intentionally not included as a current release. It has not been independently validated and does not represent the supported full-duplex conversion.
