# City Brain Convergence — Layer 1: Digital Twin & Physical World

> **Layer 1 (Twin Layer)** simulates the physical environment, generates high-frequency cryptographic telemetry for 42 IoT devices across Greater Tunis, and provides a synchronous MCP interface for city actuation and incident containment.

---

## 1. Quickstart (One-Command Deployment)

To start the complete Twin Layer ecosystem (Apache Kafka broker, Twin simulation engine, MCP Command Server, and 3D Operations Console):

```bash
docker compose up -d
```

### Endpoints at a Glance

| Service | Port (Host) | Internal Docker Address | Protocol / Purpose |
| :--- | :--- | :--- | :--- |
| **Apache Kafka** | `19092` | `kafka:9092` | Kafka Wire Protocol (Topic: `twin.sensors`, 420 msgs/s) |
| **MCP Server** | `8000` | `http://twin_layer:8000/sse` | Model Context Protocol JSON-RPC (Actuation & Queries) |
| **Adversarial Console**| `8501` | `http://twin_dashboard:8501`| Streamlit 3D Tactical Ops Dashboard |

---

## 2. System Architecture

```text
       ┌────────────────────────────────────────────────────────┐
       │             LAYER 1: DIGITAL TWIN SIMULATION           │
       │  ┌───────────────────────┐  ┌───────────────────────┐  │
       │  │ Physics Engine (10Hz) │  │  Ground Truth SQLite  │  │
       │  └──────────┬────────────┘  │     (Isolated)        │  │
       │             │               └───────────────────────┘  │
       └─────────────┼───────────────────────────▲──────────────┘
                     │ Outbound Telemetry        │ Synchronous RPC
                     │ (Ed25519 Signed)          │ (JSON-RPC)
                     ▼                           │
              ┌──────────────┐            ┌──────────────┐
              │ Kafka Broker │            │  MCP Server  │
              │(Apache Kafka)│            │  (Port 8000) │
              └──────┬───────┘            └──────▲───────┘
                     │                           │
          ┌──────────┴──────────┐     ┌──────────┴──────────┐
          ▼                     ▼     │                     │
    ┌───────────┐         ┌───────────┴─┐             ┌─────┴───────┐
    │City Brain │         │  Guardian   │             │ City Brain  │
    │ (Layer 2) │         │  (Layer 3)  │             │  (Layer 2)  │
    └───────────┘         └─────────────┘             └─────────────┘
```

---

## 3. Partner Integration Guide

For full technical specifications, JSON schemas, payload limits, and all 16 MCP tool signatures, see **[INTERFACE.md](INTERFACE.md)**.

### For Layer 2: City Brain (Traffic, Grid & Emergency Response)
1. **Consume Live Sensor Telemetry:**
   Connect standard Kafka consumer to `localhost:19092` (or `kafka:9092` in Docker) and subscribe to `twin.sensors`.
2. **Execute Actuation & Incident Control:**
   Connect to MCP Server on `http://localhost:8000/sse` and call tools:
   - `dispatch(incident_type, zone_id)`: Deploy medical/fire/police units.
   - `set_signal_plan(device_id, target_state)`: Adjust traffic lights (`green_wave`, `all_red`, `adaptive`).
   - `set_valve(device_id, target_state)`: Control drainage flood valves (`open`, `half`, `closed`).
   - `switch_grid(device_id, target_state)`: Switch substations (`grid_a`, `grid_b`, `island`).
   - `get_city_state()`: Inspect real-time status across all 6 zones.
3. **Reference Implementation:** See [mocks/mock_brain.py](mocks/mock_brain.py).

### For Layer 3: Guardian (Security, Verification & Containment)
1. **Consume Live Telemetry:**
   Subscribe to `twin.sensors` on `localhost:19092`.
2. **Verify Cryptographic Signatures:**
   Query MCP tool `get_device_key(device_id)` to fetch the device's Ed25519 public key. Verify `sig` against the canonical JSON message envelope.
3. **Trigger Containment & Isolation:**
   When an anomaly, falsified payload, or compromised device key is detected:
   - `quarantine_device(device_id)`: Blacklist and sever device network authority.
   - `isolate_device(device_id)`: Isolate physical zone segment.
   - `rollback_reading(reading_id)`: Mark poisoned reading as `rolled_back`.
   - `reinstate_device(device_id)` / `release_device(device_id)`: Restore authority after remediation.
4. **Reference Implementation:** See [mocks/mock_guardian.py](mocks/mock_guardian.py).

---

## 4. Local Development & Testing

### Running Without Docker
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest tests/ -v

# 3. Launch the Twin Engine locally
python -m twin.main

# 4. In another terminal, launch the Operations Console
streamlit run dashboard.py
```

### Automated Conformance Suite
All 41 test suites cover physical kinetics, Ed25519 signature signing/verification, adversary injection, sub-300-byte schema compliance, and MCP tool execution:
```bash
pytest tests/
```

---

## 5. Documentation Library

### Presentation-Grade PDF Guides (For Human Developers & Evaluators)
- **[Developer & Integration Guide (PDF)](docs/DEVELOPER_GUIDE.pdf)** *(7 pages)*: Full setup, MCP JSON-RPC protocol details, Kafka telemetry pipelines, Python clients, and troubleshooting.
- **[Operations & User Guide (PDF)](docs/USER_GUIDE.pdf)** *(5 pages, Illustrated)*: Complete visual tour with embedded screenshots of the 3D map, 5-minute hands-on testing tutorial, and threat injection cheatsheet.
- **[Physics & Adversary Specifications (PDF)](docs/PHYSICS_AND_ADVERSARY_SPEC.pdf)** *(3 pages)*: Mathematical diurnal models, drainage kinetics, electrical loads, and attack mechanics.

### Source Documentation & Agent Knowledge (For AI Agents & LLM Pair Programmers)
- **[Developer Guide (Markdown)](docs/DEVELOPER_GUIDE.md)**
- **[Operations & User Guide (Markdown)](docs/USER_GUIDE.md)**
- **[Physics & Adversary Specifications (Markdown)](docs/PHYSICS_AND_ADVERSARY_SPEC.md)**
- **[Interface Contract Specification (Markdown)](INTERFACE.md)**
- **[Anti-AI Humanized Editorial Rules (Markdown)](.agents/rules/HUMANIZED_STYLE_GUIDE.md)**: Writing standard based on Wikipedia guidelines, enforced by `Agent_Humanizer` in [AGENTS.md](AGENTS.md).
