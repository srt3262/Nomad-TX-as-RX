# Corrections from the older master package

The older package contained a functional custom target scaffold, but its radio and power-control block did not match the final conversion or the official Nomad definition.

| Field | Older package | Corrected master |
|---|---:|---:|
| `radio_rfsw_ctrl` | `[15, 0, 12, 8, 8, 6, 0, 5]` | Removed |
| `power_apc2` | Missing | `26` |
| `power_control` | `0` | `3` |
| Final `power_values` entry | `100` | `95` |

The corrected master retains:

- Both LR1121 radio pin groups
- Full-duplex receiver UART on GPIO3 RX / GPIO1 TX
- Fan enable on GPIO2
- Official Nomad power tables and LNA gain
- RGB LED and button pins

The installer and verifier now reject the older RF-switch and power-control values so they cannot be reintroduced silently.
