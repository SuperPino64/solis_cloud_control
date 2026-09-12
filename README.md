# Solis Cloud Control

[![HACS](https://imgio/badge/HACS-Custom-orange.svg](https://hacs.xyz/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistantvg](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/SuperPino64/solis_cloud_controlb Release](https://img.shields.io/github/v/release/SuperPino64l]()

Control your **Solis inverter** directly from **Home Assistant** using the official **Solis Cloud API**.

This integration exposes inverter controls as native Home Assistant entities, allowing you to automate charging, discharging, export limits, system settings, and other inverter functions directly from your automations and dashboards.

> ⚡ Built for users who want more than monitoring. Automate your energy management based on solar production, battery status, electricity prices, or custom Home Assistant logic.

---

## Features

✅ Native Home Assistant integration

✅ Solis Cloud API support

✅ Automatic inverter discovery

✅ Real-time inverter control entities

✅ Battery charge/discharge management

✅ Export power limit control

✅ Energy automation ready

✅ HACS compatible

---

## Screenshots

_Add screenshots here_

| Dashboard | Controls |
|------------|------------|
| docs/dashboard.png | docs/controls.png |

---

## Installation

### HACS (Recommended)

1. Open **HACS**
2. Go to **Integrations**
3. Click **⋮ → Custom repositories**
4. Add:

```
https://github.com/SuperPino64/solis_cloud_control
```

5. Select **Integration**
6. Install the integration
7. Restart Home Assistant

---

### Manual Installation

1. Download the latest release.
2. Copy:

```
custom_components/solis_cloud_control
```

to:

```
config/custom_components/
```

3. Restart Home Assistant.

---

## Configuration

1. Navigate to:

```
Settings → Devices & Services → Add Integration
```

2. Search for:

```
Solis Cloud Control
```

3. Enter:

- API Key (Key ID)
- API Secret (Token)
- Select your inverter

4. Finish setup.

---

## Getting API Credentials

To use this integration you need API access to Solis Cloud.

1. Log in to your Solis Cloud account.
2. Navigate to API Management.
3. Enable API access.
4. Generate:

- Key ID
- Key Secret

5. Use these credentials during integration setup.

> Some accounts may require activation by Solis support.

---

## Supported Functions

Depending on inverter model and firmware, available entities may include:

### Switches

- Inverter On/Off

### Numbers

- Charge current
- Discharge current
- Export power limit
- Grid settings

### Select Entities

- Energy storage mode
- Battery operating mode
- System options

### Date & Time

- Inverter clock synchronization

---

## Example Automations

### Charge Battery During Cheap Tariff

```yaml
alias: Charge Battery Cheap Energy
trigger:
  - platform: state
    entity_id: binary_sensor.energy_is_cheap
    to: "on"

action:
  - service: number.set_value
    target:
      entity_id: number.solis_charge_current
    data:
      value: 50
```

### Reduce Export Power

```yaml
alias: Limit Export
action:
  - service: number.set_value
    target:
      entity_id: number.solis_export_limit
    data:
      value: 2000
```

---

## Compatibility

The integration supports a wide range of Solis hybrid and storage inverters.

Actual available controls depend on:

- Inverter model
- Firmware version
- Solis Cloud API permissions

---

## Troubleshooting

### No inverter found

Verify:

- API credentials are correct
- API access is enabled
- Inverter appears in Solis Cloud

### Missing entities

Not all inverter models expose the same controls through the API.

### API errors

The Solis Cloud platform occasionally experiences instability. Retry after several minutes.

---





USE AT YOUR OWN RISK.

Credit go to @mkuthan

test123

