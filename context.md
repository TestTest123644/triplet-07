# PROJECT CONTEXT: TSYP 14 City Brain Convergence - Twin Layer (Layer 1)

## 1. Project Overview
We are building the **Twin Layer (Layer 1)** of a 3-layer Smart City architecture. 
- **Layer 1 (Twin):** Simulates the city, generates physics-based sensor data, applies adversarial cyber-attacks, and executes physical actuations. WE ARE BUILDING THIS.
- **Layer 2 (City Brain):** Consumes our data and decides on actions (e.g., dispatching ambulances). 
- **Layer 3 (Guardian):** Consumes our data, checks for spoofing/anomalies, and quarantines bad devices.

## 2. Core Architectural Rules
- **Parallel Data Flow:** The Twin streams live sensor data simultaneously to the Brain and the Guardian.
- **Zero Trust & Separation of Authority:** The Twin is the sole source of truth. The Twin DOES NOT accept sensor data from the other layers. It only accepts action commands.
- **Two Clocks:** 
  - `Wall-clock time`: Used ONLY for real-time latency budgets (sub-100ms processing).
  - `Simulation time` (RFC 3339 UTC): Used for all payload timestamps (`ts`). The simulated city runs on this clock.
- **Ground Truth Ledger:** The Twin must maintain a local `SQLite` database that records the *actual* physical truth and what attacks were injected. Neither the Brain nor the Guardian is allowed to access this database during the run.

## 3. The Dual Interface Contract
The Twin exposes two distinct interfaces. They cannot be mixed.

### A. The Data Stream (Kafka)
- **Role:** Push live sensor data.
- **Scale:** 6 zones, 42 devices (7 per zone). Fixed rate of 10 Hz per sensor = 420 messages/second.
- **Sensor Types:** `traffic_camera`, `water_level`, `power_load`, `air_quality`, `emergency_call`.
- **Payload Constraint:** Must strictly adhere to the ~300-byte JSON envelope.

**The Strict JSON Schema for Kafka Messages:**
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "TwinSensorReading",
    "type": "object",
    "properties": {
        "reading_id": { "type": "string" },
        "device_id": { "type": "string" },
        "device_type": { 
            "type": "string",
            "enum": ["traffic_camera", "water_level", "power_load", "air_quality", "emergency_call"]
        },
        "ts": { "type": "string", "format": "date-time" },
        "seq": { "type": "integer", "minimum": 0 },
        "value": { "type": "number" },
        "unit": { "type": "string" },
        "location": {
            "oneOf": [
                { "type": "string" },
                {
                    "type": "object",
                    "properties": {
                        "zone_id": { "type": "string" },
                        "lat": { "type": "number" },
                        "lon": { "type": "number" }
                    },
                    "required": ["zone_id"],
                    "additionalProperties": false
                }
            ]
        },
        "status": {
            "type": "string",
            "enum": ["ok", "isolated", "quarantined", "rolled_back", "modelled"]
        },
        "sig": { "type": "string", "description": "Ed25519 signature" }
    },
    "required": ["reading_id", "device_id", "device_type", "ts", "seq", "value", "unit", "location", "status", "sig"],
    "additionalProperties": false
}

B. The Command Server (MCP - Model Context Protocol)
Role: Synchronous Request/Response API for actions and queries.

Protocol: Official MCP Python SDK (JSON-RPC). This is NOT routed over Kafka.

Required MCP Tools to Implement:

Queries:

list_devices: Returns inventory and physical ranges (upper/lower bounds).

get_reading / get_readings: Fetch past data using reading_id or timestamps.

get_device_state / get_city_state: Fetch current status.

get_device_key: Returns Ed25519 public key for a given device_id.

Actuation (Called by Brain):

dispatch: (Params: incident type, zone_id)

set_signal_plan / set_valve / switch_grid: (Params: device_id, target_state)

get_command_result: (Params: idempotency_key)

Containment (Called by Guardian):

isolate_device / reinstate_device / quarantine_device / release_device: (Params: device_id)

rollback_reading: (Params: reading_id)

4. Adversary Capability Model (Simulation Engine)
The Twin simulates cyber-attacks dynamically based on injected capabilities, NOT by hardcoding symptoms.

link: Drops, delays, replays, or alters bytes (breaks signature).

rogue: Publishes data with an unknown device ID / no issued key.

device_key: Attacker holds a valid signing key; publishes arbitrary verified readings.

device_physical: Device is physically compromised (signs honestly, but perception is wrong).

actuator: Accepts commands but does not execute them.

sensor_fault: Honest malfunction (drift, stuck values, dropouts).

