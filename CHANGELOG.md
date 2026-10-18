# CHANGELOG - TSYP 14 City Brain Convergence (Twin Layer)

All notable milestones and changes to the Twin Layer (Layer 1) are documented in this file.

## [1.5.1] - Presentation-Grade PDF Generation & Subagent Rule Integration
### Added
- **Automated PDF Compilation Pipeline (`scripts/generate_docs_pdf.py`)**:
  - Implemented automated PDF generator using `markdown` and `xhtml2pdf.pisa` with custom executive CSS typography, running headers/footers (`Page X of Y`), and embedded high-resolution screenshots.
  - Generated presentation-ready PDF manuals:
    - `docs/DEVELOPER_GUIDE.pdf` (7 pages)
    - `docs/USER_GUIDE.pdf` (5 pages, illustrated with 3D map and neighborhood cards)
    - `docs/PHYSICS_AND_ADVERSARY_SPEC.pdf` (3 pages)
  - Preprocessed ASCII box diagrams and math symbols for crisp rendering in Courier.

## [1.5.0] - Comprehensive Documentation Suite
### Added
- **Developer & Integration Manual (`docs/DEVELOPER_GUIDE.md`)**:
  - Authored comprehensive developer documentation covering architecture, Docker vs local execution, MCP protocol and Python client integration, Kafka streaming parameters, Ed25519 canonical signature verification routines, 30-second benchmark reproduction, and troubleshooting.
- **Operations & User Guide with Screenshots (`docs/USER_GUIDE.md`)**:
  - Created illustrated operational guide embedding product screenshots of the 3D Greater Tunis tactical map, neighborhood status cards, and cartography detail.
  - Included a 5-minute hands-on tutorial guiding users through baseline verification, attack injection across all 6 capabilities, divergence inspection, pitch presets, and disarm recovery.
- **Physical Simulation & Adversary Specification (`docs/PHYSICS_AND_ADVERSARY_SPEC.md`)**:
  - Documented physical differential equations, bimodal diurnal traffic curves, gravity water drainage kinetics, electrical load profiles, and attack mechanics.

## [1.4.0] - Official Apache Kafka Transition & Partner Onboarding Package
### Added
- **Official Apache Kafka Integration (`docker-compose.yml`, `Dockerfile`, `INTERFACE.md`)**:
  - Migrated the message broker from Redpanda to official Apache Kafka (`apache/kafka:latest`) operating natively in KRaft mode (no ZooKeeper dependency).
  - Configured broker with dual listeners: internal `PLAINTEXT://kafka:9092` for Docker container-to-container communication, and external `EXTERNAL://localhost:19092` mapped to host machine.
  - Implemented health checks querying `/opt/kafka/bin/kafka-broker-api-versions.sh` to ensure deterministic container startup ordering.
  - Updated `Dockerfile` default bootstrap server to `kafka:9092` and refreshed architecture diagrams and connection parameters in `INTERFACE.md`.
- **Root Repository Onboarding & Architecture Guide (`README.md`)**:
  - Published comprehensive GitHub landing documentation containing 1-command startup (`docker compose up -d`), endpoint cheatsheet, system topology diagram, and partner integration instructions for Layer 2 (City Brain) and Layer 3 (Guardian).
- **Subagent Code Review & Conformance Verification**:
  - Full automated QA test suite verified at 41/41 tests passing (100%).
  - Verified Phase 0 contract conformance: sub-300-byte payload budgets, RFC 3339 UTC simulation timestamps, and complete database isolation.

## [1.3.3] - DOM QA Verification, Modernized Sizing & State Synchronization
### Added
- **Automated DOM QA Testing Suite (`tests/test_dashboard_dom.py`)**:
  - Implemented automated DOM tree inspection using Streamlit's official `AppTest` framework, verifying clean component mounting, multi-tab layout, scoreboard metrics, preset exploit triggering, and disarm state transitions.
- **Database Attack Deactivation Synchronization (`twin/db_ledger.py`, `twin/simulation.py`)**:
  - Added `deactivate_attack` and `deactivate_all_attacks` to ensure all historical and current attack records in `attacks_injected` are marked inactive upon disarming, guaranteeing exact 0-count scoreboard recovery.
- **Modernized Streamlit Component Sizing (`dashboard.py`)**:
  - Replaced deprecated `use_container_width=True` on `st.altair_chart` and `st.dataframe` with modern `width="stretch"` syntax, eliminating console deprecation warnings.
- **Fixture State Decontamination (`tests/test_demo_flow.py`, `tests/test_qa_conformance.py`)**:
  - Added teardown resets for `_ACTIVE_SIMULATOR` across all pytest fixtures, ensuring complete isolation across all 41 test suites.

## [1.3.2] - Exhaustive Codebase Audit, Pitch Presets & Presentation Conformance
### Added
- **Hackathon Pitch Demo Presets (`dashboard.py`)**:
  - Added 6 calibrated one-click attack presets in the sidebar enabling presenters to demonstrate every capability live with single-click execution during the jury pitch.
  - Scenarios cover Physical Spoofing (Downtown), Compromised Key Forgery (Industrial), Link Signature Tampering (Harbor), Rogue Transmitter (West Hills), Sensor Drift (University), and Actuator Non-Execution (Flood Valve).
- **Time-Filtered Reading Queries (`twin/mcp_server.py`, `INTERFACE.md`)**:
  - Implemented `since_ts` RFC 3339 UTC timestamp filter in the `get_readings` MCP tool, fulfilling contract requirements for temporal telemetry queries.
- **Runnable Mock Client Demonstrators (`mocks/mock_brain.py`, `mocks/mock_guardian.py`)**:
  - Added standalone `__main__` entry points demonstrating zero-trust cryptographic signature validation, link corruption interception, rogue transmitter quarantine, and automated threshold-based smart city actuation.
- **End-to-End Presentation Conformance Test (`tests/test_demo_flow.py`)**:
  - Added comprehensive automated test validating all 10 stages of the pitch demo workflow from baseline to multi-exploit injection, Guardian interception, Brain actuation, disarm recovery, and full MCP tool surface verification. Test suite now stands at 39/39 passed (100%).
- **Dependency Rigor & Container Resilience (`requirements.txt`, `twin/main.py`)**:
  - Explicitly pinned direct dependencies (`pydeck`, `altair`, `uvicorn`, `starlette`) in `requirements.txt`.
  - Added configurable `KAFKA_WAIT_RETRIES` environment variable and graceful fallback to local sink buffer mode when running standalone without Redpanda.

## [1.3.1] - Map Tile Typography Fix, Sector Realignment & Autonomous Threat Coordinator
### Added
- **Complete Emoji Removal & Enterprise Cyber Ops UI**:
  - Eliminated all emojis across headers, tabs, metric cards, status badges, buttons, and alert logs.
  - Replaced with high-contrast tactical status badges (`[NOMINAL]`, `[CRITICAL THREAT]`, `[ALERT]`, `[TWIN]`), monospace typography (`JetBrains Mono`), and Palantir/Falcon defense-grade ops aesthetics.
- **Geographic Realignment & Zero Water Collisions (`twin/simulation.py`, `dashboard.py`)**:
  - Realigned all 6 metropolitan neighborhood sectors onto verified dry land in Greater Tunis:
    - `Downtown Financial`: `36.8000, 10.1800` (downtown commercial center)
    - `Port & Coastal Harbor`: `36.8050, 10.2700` (harbor docks and shipping canal)
    - `North Industrial Park`: `36.8480, 10.2050` (Charguia / Ariana Sud industrial park)
    - `West Residential Hills`: `36.8150, 10.1300` (Bardo / Manouba hills, completely relocated away from Sebkhet Sijoumi lake)
    - `Central University & Med`: `36.8320, 10.1550` (El Manar university & Rabta medical campus)
    - `South Logistics Hub`: `36.7550, 10.2200` (Ben Arous freight rail terminal)
  - Automatically re-seeded all 42 IoT sensors in `ground_truth.db` with the updated non-colliding coordinates.
- **Tile Typography Fix (Resolving Disconnected Arabic Text)**:
  - Switched PyDeck basemap style to `CARTO_DARK_NO_LABELS` (`https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json`).
  - Completely eliminates the Mapbox GL glyph bug that caused Arabic map labels to render as disconnected isolated letters (`ي د ي ب...`).
  - Basemap now renders crisp dark vector roads, coastlines, and building footprints, while our custom PyDeck text layer renders clean English neighborhood callouts.
- **Active Threat Integration & Autonomous Simulation Clock**:
  - Updated `fetch_geospatial_sensors()` and `fetch_neighborhood_summaries()` to directly cross-reference active attacks from `attacks_injected` in addition to historical ledger rows.
  - When an attack is executed in standalone mode (without `twin.main`), `dashboard.py` automatically advances 5 simulation ticks on the local `CitySimulator`, immediately updating `readings_truth` with physical vs broadcast discrepancies.
  - Added "PULSE 10 TICKS (+1.0s)" control in the sidebar for manual on-demand clock advancement.
  - Added dual-mode Engine Status banner displaying whether the system is connected to the distributed `twin_layer` daemon or running in autonomous local testing mode.

## [1.3.0] - 3D Geospatial Digital Twin & Advanced Telemetry Visualization
### Added
- **Interactive 3D Digital Twin Map (`dashboard.py`, PyDeck)**:
  - Spawned `Agent_UI` to implement a 3D geospatial operations deck centered on Tunis metropolitan area (`36.802, 10.175`).
  - **3D Sensor Columns & Elevation:** Renders all 42 IoT sensors in 3D space with column heights scaled dynamically to physical telemetry values.
  - **Threat Highlighting & Beacon Rings:** Nominal sensors rendered in neon cyan (`[0, 229, 255]`); attacked sensors elevated and illuminated in glowing crimson (`[255, 45, 85]`) with pulsating danger scatter halos.
  - **Neighborhood Radar Centroids:** Displays labeled neighborhood centroids ("Downtown Financial", "Port & Coastal Harbor", "North Industrial Park", "West Residential Hills", "Central University & Med", "South Logistics Hub") with dynamic translucent buffer radar halos that turn red when an exploit is active within that zone.
  - **Interactive Tooltips & Filtering:** Rich HTML tooltips showing Device ID, Type, Neighborhood, Physical Truth, Broadcast Stream, and Exploit status, with multi-level filtering by neighborhood, sensor type, and 3D camera pitch.
- **Neighborhood Operational Health Matrix**:
  - 6-card operational grid displaying real-time aggregated metrics per neighborhood: Average Traffic, Maximum Water Level, Total Power Load, AQI, and active exploit counts.
- **Telemetry & Attack Divergence Curves (Altair)**:
  - Real-time time-series chart comparing **Physical Ground Truth** against the **Broadcast Telemetry Stream**.
  - Visually illustrates divergence intervals during drift, physical spoofing, stuck sensors, and signature forgery attacks.
  - Computes divergence analytics: Latest Physical Truth, Latest Broadcast, Current Discrepancy, and Tampered Frames count.
- **Enhanced Glassmorphism Aesthetics & Micro-Animations**:
  - Radial cyberpunk backdrop gradient, glassmorphic cards with `backdrop-filter: blur(10px)`, and CSS threat pulse animations (`@keyframes pulse-threat`).
- **Comprehensive Conformance Tests (`tests/test_dashboard.py`)**:
  - Added `test_dashboard_geospatial_and_divergence` validating 3D sensor coordinates, neighborhood aggregations, and time-series divergence. Full test suite passing at 38/38.

## [1.2.0] - Adversarial Console & Visualization (Challenge Rule R3)
### Added
- **Interactive Streamlit Adversarial Console (`dashboard.py`)**:
  - Spawned `Agent_UI` to implement a high-tech operations dashboard fulfilling Challenge Rule R3.
  - **Header/Scoreboard:** Live aggregated metrics displaying Total Telemetry Readings, Active Incidents (detected physical/broadcast discrepancies), Active Attacks, and strict RFC 3339 UTC Simulated Time (`ts`).
  - **Red Team Controls (Sidebar):** Interactive adversary injection panel targeting any of the 42 registered IoT sensors with all 6 Phase 0 capabilities (`link`, `rogue`, `device_key`, `device_physical`, `actuator`, `sensor_fault`) and dynamic parameter controls (drift rates, stuck values, tamper offsets, drop/corrupt/replay modes). Includes active threat manifest with live cancellation buttons.
  - **The Truth Ledger (Main View):** Real-time auto-refreshing table displaying the last 20 readings directly from `ground_truth.db`. Highlights discrepancies between physical ground truth and broadcast stream in vivid red (`[ALERT] ATTACK DETECTED` vs `[OK] NOMINAL`).
  - **Live Feed (Simulation Time Timeline):** Real-time scrolling event log displaying chronological audit events ordered by Simulation Time (`ts`) with automated alert categorization.
  - **Strict Read-Only Database Isolation:** Connects to `ground_truth.db` via URI `?mode=ro`, preventing the console from mutating the ground truth ledger.
- **Internal REST Attack API (`twin/main.py`)**:
  - Mounted internal administrative endpoints on the unified Starlette application: `POST /api/attack/inject`, `POST /api/attack/clear`, `GET /api/attack/active`, `GET /api/status`.
  - Enables seamless inter-container communication from the dashboard to the running physics simulator without exposing ground-truth write access or breaking MCP server isolation.
- **Docker Compose Multi-Container Orchestration (`docker-compose.yml`, `Dockerfile`)**:
  - Added `dashboard` service running Streamlit on port `8501:8501`.
  - Configured shared volume `shared_data` allowing the dashboard container read-only access to `ground_truth.db` alongside the `twin_layer` container.
- **Automated Conformance & Unit Testing (`tests/test_dashboard.py`)**:
  - Added 3 comprehensive automated tests validating read-only SQLite isolation, REST attack API injection and clearing, and dashboard interfacing. Full test suite passing at 37/37.

## [1.1.0] - Partner Integration Readiness (Challenge Rule R1)
### Added
- **Interface Contract Documentation (`INTERFACE.md`)**:
  - Published comprehensive integration specification fulfilling Challenge Rule R1 for Layer 2 (City Brain) and Layer 3 (Guardian).
  - Fully documented the exact Kafka outbound `schema.json` with Ed25519 canonical signature verification Python routines.
  - Detailed parameter and return schemas for all 16 MCP endpoints across Queries (`list_devices`, `get_reading`, `get_readings`, `get_device_state`, `get_city_state`, `get_device_key`), Actuations (`dispatch`, `set_signal_plan`, `set_valve`, `switch_grid`, `get_command_result`), and Containment (`isolate_device`, `reinstate_device`, `quarantine_device`, `release_device`, `rollback_reading`).
  - Cataloged physical measurement ranges and actuation control bindings for all 42 devices across 6 city zones.
- **Local Containerized Environment (`docker-compose.yml`, `Dockerfile`, `twin/main.py`)**:
  - Integrated `redpandadata/redpanda:v26.2.4` Kafka broker configured in production mode with dual internal (`redpanda:9092`) and external (`localhost:19092`) listeners.
  - Built production `Dockerfile` running on lightweight Python 3.11 with non-root security hygiene.
  - Created unified runtime runner `twin/main.py` executing the 10 Hz Kafka producer loop and Starlette/Uvicorn MCP Server (`0.0.0.0:8000`) simultaneously on a shared asyncio event loop.
  - Bridge network `twin_network` configured ensuring Twin container publishes to Redpanda broker, with MCP port `8000` and Kafka port `19092` exposed to host machine.

## [1.0.0] - Phase 6 Complete (Full System Release)
### Added
- **Mock Security & Decision Clients (`mocks/mock_guardian.py`, `mocks/mock_brain.py`)**:
  - `MockGuardian` (Layer 3): Consumes Kafka stream, fetches Ed25519 public keys via MCP `get_device_key`, verifies cryptographic signatures, and issues MCP `quarantine_device` / `rollback_reading` commands upon detecting rogue devices or corrupted link bytes.
  - `MockCityBrain` (Layer 2): Autonomous actuation agent consuming telemetry and invoking MCP `dispatch`, `set_valve`, `set_signal_plan`, and `switch_grid`.
- **High-Throughput 30-Second Stress Benchmark (`tests/test_qa_conformance.py`)**:
  - Executed 300 simulation cycles (30.0 simulated seconds at 10 Hz across 42 devices = 12,600 messages).
  - Achieved sustained production throughput of **2,605.4 msgs/sec** (surpassing the 420 msgs/sec benchmark by >6x).
  - Zero memory leaks confirmed (RSS delta: 23.39 MB).
- **Physical Truth Integrity Locking**:
  - Validated that SQLite Ground Truth ledger accurately recorded true physical reality while external stream broadcasted a `device_physical` attack.
- **Final Security & Architecture Audit**:
  - Verified 100% isolation of SQLite Truth Ledger from MCP server.
  - Verified zero wall-clock time leakage into payload timestamps.
  - 100% test pass rate across all 34 automated unit and integration tests.

## Phase 5 Complete
### Added
- **Adversary Capability Model (`twin/simulation.py`)**:
  - Implemented dynamic attack injection layer with zero hardcoding: `inject_attack()`, `clear_attack()`, `clear_all_attacks()`.
  - Implemented all 6 adversary capability triggers:
    - `link`: Byte corruption (signature invalidation), packet drop, and packet replay.
    - `rogue`: Unauthorized device broadcasts with unissued signing keys.
    - `device_key`: Stolen valid key forge attack (verified signature over physical falsehood).
    - `device_physical`: Compromised sensor perception with honest firmware signature.
    - `actuator`: Command acknowledgement without physical execution.
    - `sensor_fault`: Hardware drift, stuck readings, and intermittent dropouts.
  - Automated dual logging in SQLite Truth Ledger: preserves true physical state and simultaneously records broadcast values and injected attack tags.
- **Phase 5 Tests (`tests/test_adversary.py`)**: 6 automated tests validating every capability and ledger state isolation.

## Phase 4 Complete
### Added
- **MCP Synchronous Command Server (`twin/mcp_server.py`)**:
  - Implemented official MCP Python SDK `MCPServer` instance exposing synchronous tool endpoints for City Brain (Layer 2) and Guardian (Layer 3).
  - Implemented Queries: `list_devices`, `get_device_key`, `get_device_state`, `get_city_state`, `get_reading`, `get_readings`.
  - Implemented Actuations: `dispatch`, `set_signal_plan`, `set_valve`, `switch_grid`, and idempotent retrieval `get_command_result`.
  - Implemented Containment: `isolate_device`, `quarantine_device`, `reinstate_device`, `release_device`, and `rollback_reading`.
  - Verified 100% cryptographic and state isolation: MCP endpoints cannot read or query the local SQLite Ground Truth ledger.
- **Phase 4 Tests (`tests/test_mcp_server.py`)**: 7 automated tests validating queries, actuation impacts, containment operations, and ledger isolation.

## Phase 3 Complete
### Added
- **Cryptography & Kafka Streaming (`twin/kafka_streamer.py`, `twin/crypto_utils.py`)**:
  - Pydantic schema validation strictly matching `context.md` `TwinSensorReading` schema with `extra="forbid"`.
  - Canonical deterministic stringification and Ed25519 digital signature attached to every outbound payload.
  - Strict 300-byte budget compliance verified across all 42 devices (range: 288B - 299B, average: 294.1B).
  - Outbound-only `KafkaStreamer` producer engine utilizing `confluent-kafka` configured for 420 msgs/sec throughput.
- **Phase 3 Tests (`tests/test_kafka_streamer.py`)**: 5 automated tests for schema validation, forbidden fields, signature verification, and payload size benchmarking.

## Phase 2 Complete
### Added
- **Core Physics & Clock (`twin/simulation.py`)**:
  - Implemented dual-clock engine (`SimulationClock`) enforcing strict RFC 3339 UTC timestamps and 10 Hz wall-clock pacing.
  - Generated complete device inventory: exactly 42 devices across 6 zones (7 per zone) covering all 5 sensor types (`traffic_camera`, `water_level`, `power_load`, `air_quality`, `emergency_call`).
  - Implemented differential mathematical formulas for normal city behavior: diurnal traffic curves, water valve drainage dynamics, substation load variation, traffic-correlated air quality dispersion, and emergency response decay.
  - Automated SQLite ledger integration: true physical state recorded per tick into `readings_truth`.
  - Added actuation and containment handlers (`handle_dispatch`, `handle_set_valve`, `handle_set_signal_plan`, `handle_switch_grid`, `update_device_status`).
- **Phase 2 Tests (`tests/test_simulation.py`)**: Added 5 comprehensive automated tests for clock precision, inventory, tick loops, and actuation impact.

## Phase 1 Complete
### Added
- **Project Structure & Scaffolding**: Initialized `/twin` core package (`simulation.py`, `kafka_streamer.py`, `mcp_server.py`, `crypto_utils.py`, `db_ledger.py`), `/tests`, and `/mocks`.
- **Dependency Management**: Created `requirements.txt` containing `confluent-kafka`, `mcp`, `pydantic`, `cryptography`, and `pytest`. Successfully installed and verified all dependencies in the runtime environment.
- **Ground Truth Ledger (`twin/db_ledger.py`)**: Implemented local SQLite database schema isolated from Layer 2 (Brain) and Layer 3 (Guardian), with dedicated tables:
  - `devices`: Comprehensive physical metadata, zones, measurement bounds, and public keys.
  - `readings_truth`: Ground-truth values vs. broadcast values, Simulation Time timestamps, sequence numbers, and attack flags.
  - `attacks_injected`: Adversary capability records, parameters, simulation timestamps, and activation states.
- **Cryptographic Foundations (`twin/crypto_utils.py`)**: Implemented Ed25519 keypair generation, canonical JSON payload signing, and public key verification.
- **Automated Test Suite**: Added test suites (`tests/test_ledger.py` and `tests/test_crypto.py`), verified with 100% pass rate.
- **Audit Logs**: Initialized `DEV_LOGS.md` and `CHANGELOG.md` under `Agent_Orchestrator` management.
