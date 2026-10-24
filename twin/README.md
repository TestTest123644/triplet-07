# Layer 1: Digital Twin & Physical World Simulation

The **Twin Layer** simulates the smart city physical environment, generates high-frequency telemetry, signs outgoing data cryptographically, and executes actuation/containment commands.

---

## 1. Responsibilities
- **Physical World Simulation (10 Hz):** Models 42 devices across 6 geographic zones in Greater Tunis spanning 5 sensor types (`traffic_camera`, `water_level`, `power_load`, `air_quality`, `emergency_call`).
- **Telemetry Streaming (Kafka):** Broadcasts 420 msgs/s to Apache Kafka topic `twin.sensors`. Every payload conforms to the sub-300-byte schema and includes a unique Ed25519 digital signature.
- **Synchronous Commands (MCP):** Exposes an official Model Context Protocol (MCP) server on port `8000` (`http://localhost:8000/sse`) for device discovery (`list_devices`), cryptographic key retrieval (`get_device_key`), actuation (`dispatch`, `set_valve`, `switch_grid`, `set_signal_plan`), and containment (`quarantine_device`, `isolate_device`, `rollback_reading`).
- **Red Team Adversary Engine:** Injects 6 cyber-physical attack capabilities (`link`, `rogue`, `device_key`, `device_physical`, `actuator`, `sensor_fault`).
- **Ground Truth Ledger:** Logs uncompromised ground truth and attack events into an isolated local SQLite database (`ground_truth.db`).

---

## 2. Directory Layout
```
twin/
├── __init__.py           # Package exports
├── simulation.py         # 10 Hz physical world simulation and diurnal kinetics
├── mcp_server.py         # MCP JSON-RPC Server (Port 8000)
├── kafka_streamer.py     # High-throughput Kafka producer with Ed25519 signing
├── crypto_utils.py       # Ed25519 signing, canonical JSON formatting, and verification
├── db_ledger.py          # SQLite ground-truth storage (isolated)
├── main.py               # Twin runtime orchestrator
├── INTERFACE.md          # Complete API contract and Kafka schema
└── README.md             # This document
```

---

## 3. Running the Twin Layer

### Using Docker Compose (Recommended)
From the repository root:
```bash
docker compose up -d
```
Starts Apache Kafka on `localhost:19092` and the Twin Layer engine on `http://localhost:8000/sse`.

### Running Locally with Python
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run test suite
pytest tests/

# 3. Launch Twin simulation
python -m twin.main
```
