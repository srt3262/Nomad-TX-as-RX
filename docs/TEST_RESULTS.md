# Test status

## Confirmed

- The Nomad conversion bound successfully and operated as an ExpressLRS receiver.
- The current design uses the two-wire full-duplex UART path: GPIO3 RX and GPIO1 TX.
- Both LR1121 radio definitions are retained for Gemini Xrossband operation.
- The source installer and verifier pass automated tests against a representative ExpressLRS hardware tree.

## Power-source observation

During the July 2026 test series, telemetry range was poor while the Nomad was powered through USB-C, including with a high-wattage USB supply. Setting telemetry power to fixed 500 mW or 1 W did not resolve that behavior.

With the module powered from a 12 V supply on a bench inside a house, telemetry remained connected to approximately one mile while the transmitting radio was inside a vehicle. This was an informal real-world observation, not a controlled range test or a guaranteed performance specification.

## Still needing independent validation

- Repeatable conducted or open-field RF measurements
- Thermal testing at sustained high telemetry power
- GPIO2 fan-control behavior across telemetry power levels
- Flight-controller CRSF and MAVLink interoperability
- Single-wire S.Port operation
- Recovery testing on additional Nomad hardware revisions
