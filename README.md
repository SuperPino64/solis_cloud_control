# Solis Cloud Control

Control your **Solis inverter** directly from **Home Assistant** using the official **Solis Cloud API**.

This integration exposes inverter controls as native Home Assistant entities, allowing you to automate charging, discharging, export limits, system settings, and other inverter functions directly from your automations and dashboards.

> ⚡ Built for users who want more than monitoring. Automate your energy management based on solar production, battery status, electricity prices, or custom Home Assistant logic.

---

## Features

✅ Solis Cloud API support

✅ Automatic inverter discovery

✅ Real-time inverter control entities

✅ Export power limit control





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


## Supported Functions

Depending on inverter model and firmware, available entities may include:

### Switches

- Inverter On/Off

### Numbers

- Export power limit





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

