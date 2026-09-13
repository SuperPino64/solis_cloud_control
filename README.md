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

✅ Inverter temperature monitoring

✅ AC output power monitoring

✅ Daily energy production monitoring

✅ Lifetime energy production monitoring

✅ Automatic retry handling for Solis Cloud API errors

✅ Native Home Assistant entities

### Available Entities

#### Sensors

| Entity | Description |
|----------|-------------|
| AC Output Power | Current inverter AC output power (kW) |
| Inverter Temperature | Current inverter internal temperature (°C) |
| Today Energy | Energy generated today |
| Total Energy | Lifetime generated energy |

#### DateTime

| Entity | Description |
|----------|-------------|
| Inverter Time | Internal inverter clock |

#### Numbers

| Entity | Description |
|----------|-------------|
| Export Power Limit | Set inverter export power limit |

#### Switches

| Entity | Description |
|----------|-------------|
| Inverter On/Off | Enable or disable inverter output |

### Polling & Update Rate

The integration retrieves data from the official Solis Cloud API.

Default behavior:

- Polling interval: **3 minutes**
- API timeout: **60 seconds**
- Automatic retry handling for temporary Solis Cloud API failures (timeouts and 502 responses)

> Note: Solis Cloud occasionally experiences API slowdowns or temporary gateway errors. The integration will automatically retry failed requests when possible.

---

## Installation

### HACS (Recommended)

1. Open **HACS**
2. Go to **Integrations**
3. Click **⋮ → Custom repositories**
