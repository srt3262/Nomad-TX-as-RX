# Contributing

Contributions that improve reproducibility, hardware support, testing, documentation, or recovery are welcome.

## Before opening a pull request

1. Base changes on the current default branch.
2. Keep the two hardware layouts identical:
   - `RX/Radiomaster Nomad RX FCC.json`
   - `hardware-upload/hardware-nomad-rx-fcc-v4-fan.json`
3. Run:

   ```bash
   python -m compileall -q install_nomad_rx_target.py verify_nomad_rx_target.py tests
   python -m unittest discover -s tests -v
   ```

4. Explain which ExpressLRS version and commit were used.
5. Update `CHANGELOG.md` for user-visible behavior changes.

## Hardware test reports

Please include:

- Nomad hardware revision, if known
- ExpressLRS version and commit
- Exact active `hardware.json`
- Wiring and serial protocol
- Input voltage and power source
- Selected band or Gemini mode
- Telemetry power and packet rate
- Antenna arrangement and test environment
- Reproduction steps, logs, RSSI/SNR/LQ data, and observed result

Do not report an informal range drive as a guaranteed range specification.

## Scope

The default target is the two-wire full-duplex UART conversion on GPIO3 RX and GPIO1 TX. Experimental single-wire S.Port work should remain clearly labeled and separate until independently verified.

By contributing, you agree that your contribution is licensed under GPL-3.0-or-later.
