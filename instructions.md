# BUILD ROADMAP & INSTRUCTIONS

## 📋 Execution Rules for Agents
1. **Linear Progression:** Tasks must be executed in the exact order specified below. Do not jump to Phase 3 before Phase 2 is reviewed and approved by `Agent_Reviewer`.
2. **Review Gates:** At the end of every Phase, `Agent_Reviewer` MUST validate the code against `context.md` and `agents.md`.
3. **No Placeholders:** Write production-ready, fully typed Python code. Do not leave `TODO` or `pass` blocks in the core logic.

## 📝 Logging & State Management Protocol
`Agent_Orchestrator` must maintain two files in the root directory:
- `CHANGELOG.md`: High-level summary of completed features and milestones.
- `DEV_LOGS.md`: Detailed technical log of decisions made, schema validations, port configurations, and debug output from tests. Update this file after EVERY step.

---

## 🚀 PHASE 1: Project Scaffolding & Dependencies
**Assignees:** `Agent_Orchestrator`
1. Initialize the Python project structure:
   - `/twin` (Core package)
     - `simulation.py`
     - `kafka_streamer.py`
     - `mcp_server.py`
     - `crypto_utils.py`
     - `db_ledger.py`
   - `/tests`
   - `/mocks`
2. Create `requirements.txt` (must include `confluent-kafka`, `mcp`, `pydantic`, `cryptography`).
3. Set up the local SQLite database schema for the Ground Truth Ledger (tables for `devices`, `readings_truth`, `attacks_injected`).

## ⚙️ PHASE 2: Core Physics & Clock (The Simulator)
**Assignees:** `Agent_Physics`
1. **Clock System:** Implement the dual-clock system. Create a strict `get_sim_time()` function that returns RFC 3339 UTC strings, and enforce that wall-clock time is ONLY used for cycle pacing (10 Hz).
2. **Device Inventory:** Generate the 42 devices (7 across 6 zones) spanning the 5 types.
3. **Tick Loop:** Implement the 10 Hz fixed-timestep loop. Calculate standard mathematical formulas for normal city behavior (e.g., normal water levels, normal traffic density).
4. **Ledger Integration:** Every simulated tick must write the *true* state to the SQLite ledger via `db_ledger.py`.

## 🔐 PHASE 3: Crypto & Kafka Streaming
**Assignees:** `Agent_Kafka`, `Agent_Reviewer`
1. **Cryptography:** In `crypto_utils.py`, generate Ed25519 keypairs for all 42 devices. Implement a payload signing function that deterministically stringifies the JSON and signs it.
2. **Schema Enforcement:** Use `pydantic` to define the 300-byte `schema.json` from `context.md`. Validate all outgoing data against this model.
3. **Producer Setup:** Configure `confluent-kafka` producer. Hook it into the 10 Hz simulation loop to stream the signed JSON envelopes.
4. **REVIEW GATE:** `Agent_Reviewer` checks payload size (<300 bytes) and verifies the schema is 100% compliant with `context.md`.

## 📡 PHASE 4: MCP Command Server
**Assignees:** `Agent_MCP`
1. Initialize the MCP Server using the Official Python SDK.
2. Implement **Queries**: `list_devices`, `get_reading`, `get_device_state`, `get_device_key`. (Ensure `get_device_key` returns the correct public key generated in Phase 3).
3. Implement **Actuation**: `dispatch`, `set_signal_plan`, `set_valve`, `switch_grid`. These must interact with `Agent_Physics` to change the simulation state (e.g., closing a valve stops water flow in the next tick).
4. Implement **Containment**: `isolate_device`, `quarantine_device`, `rollback_reading`. These must update the device's status field in the outgoing Kafka JSON envelope.

## 🦹‍♂️ PHASE 5: Adversary Capability Model
**Assignees:** `Agent_Physics`
1. Introduce the attack injection layer into the simulation loop.
2. Implement the 6 capability triggers: `link`, `rogue`, `device_key`, `device_physical`, `actuator`, `sensor_fault`.
3. When an attack is triggered, alter the data *before* it hits the Kafka streamer, but ensure the SQLite Truth Ledger records both the *fake* value sent to Kafka and the *true* physical value.

## 🧪 PHASE 6: QA & Conformance Testing
**Assignees:** `Agent_QA`, `Agent_Reviewer`
1. Write a `mock_guardian.py` that listens to the Kafka topic, fetches a key via MCP `get_device_key`, and verifies the Ed25519 signature of the stream.
2. Run a 30-second stress test simulating all 42 devices at 10 Hz (420 msgs/sec). Log memory/CPU usage to `DEV_LOGS.md`.
3. Assert that the SQLite database accurately locked the truth while the stream broadcasted a `device_physical` attack.
4. **FINAL REVIEW GATE:** `Agent_Reviewer` ensures zero cross-contamination (MCP cannot read the truth ledger, Kafka schema is perfect, no wall-clock time in payloads).