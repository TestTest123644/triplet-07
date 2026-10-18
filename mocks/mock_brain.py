"""Mock City Brain (Layer 2) Client.

Assigned to: Agent_QA
Simulates Layer 2 City Brain:
1. Ingests sensor telemetry stream from Twin Layer.
2. Evaluates city operational thresholds.
3. Invokes MCP synchronous actuation endpoints:
   - 'dispatch' on emergency call surge.
   - 'set_valve' on high water levels.
   - 'set_signal_plan' during traffic congestion.
   - 'switch_grid' during peak electrical demand.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from twin.mcp_server import (
    dispatch,
    get_city_state,
    list_devices,
    set_signal_plan,
    set_valve,
    switch_grid,
)

logger = logging.getLogger("mock_brain")


class MockCityBrain:
    """Mock City Brain decision engine orchestrating smart city actuations via MCP."""

    def __init__(self):
        self.dispatches_sent = 0
        self.valve_commands_sent = 0
        self.signal_plans_sent = 0
        self.grid_switches_sent = 0
        self.actuations_log: List[Dict[str, Any]] = []

    def evaluate_reading(self, payload_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate incoming sensor reading and trigger appropriate actuation if threshold crossed."""
        actions_taken = []
        dtype = payload_dict.get("device_type")
        val = payload_dict.get("value", 0.0)
        dev_id = payload_dict.get("device_id")
        loc = payload_dict.get("location")
        zone_id = loc if isinstance(loc, str) else (loc.get("zone_id") if isinstance(loc, dict) else "zone-1")

        # 1. Flood Defense: Open valve if water level exceeds 4.5 meters
        if dtype == "water_level" and val > 4.5:
            res = set_valve(device_id=dev_id, target_state="open", idempotency_key=f"act-valve-{dev_id}")
            self.valve_commands_sent += 1
            action = {"type": "set_valve", "device_id": dev_id, "result": res}
            self.actuations_log.append(action)
            actions_taken.append(action)

        # 2. Traffic Flow: Trigger green wave if vehicles/min exceeds 90
        elif dtype == "traffic_camera" and val > 90.0:
            res = set_signal_plan(device_id=dev_id, target_state="green_wave", idempotency_key=f"act-sig-{dev_id}")
            self.signal_plans_sent += 1
            action = {"type": "set_signal_plan", "device_id": dev_id, "result": res}
            self.actuations_log.append(action)
            actions_taken.append(action)

        # 3. Emergency Surge: Dispatch ambulance / fire if call volume > 5 calls/min
        elif dtype == "emergency_call" and val > 5.0:
            res = dispatch(incident_type="medical_surge", zone_id=zone_id, idempotency_key=f"act-disp-{zone_id}")
            self.dispatches_sent += 1
            action = {"type": "dispatch", "zone_id": zone_id, "result": res}
            self.actuations_log.append(action)
            actions_taken.append(action)

        # 4. Power Load Shedding / Routing: Switch grid if load > 95 MW
        elif dtype == "power_load" and val > 95.0:
            res = switch_grid(device_id=dev_id, target_state="grid_b", idempotency_key=f"act-grid-{dev_id}")
            self.grid_switches_sent += 1
            action = {"type": "switch_grid", "device_id": dev_id, "result": res}
            self.actuations_log.append(action)
            actions_taken.append(action)

        return actions_taken


if __name__ == "__main__":
    print("[MOCK CITY BRAIN] Initializing Layer 2 autonomous actuation engine...")
    brain = MockCityBrain()
    print("[MOCK CITY BRAIN] Connected to MCP Command Server tools.")

    test_samples = [
        {"device_id": "z1-tc1", "device_type": "traffic_camera", "value": 115.0, "location": "zone-1"},
        {"device_id": "z2-wl1", "device_type": "water_level", "value": 5.8, "location": "zone-2"},
        {"device_id": "z3-pl1", "device_type": "power_load", "value": 98.4, "location": "zone-3"},
        {"device_id": "z4-ec1", "device_type": "emergency_call", "value": 8.0, "location": "zone-4"},
    ]

    for sample in test_samples:
        print(f"\n[STREAM INGEST] Evaluating {sample['device_id']} ({sample['device_type']} = {sample['value']})...")
        actions = brain.evaluate_reading(sample)
        for act in actions:
            print(f"  --> [ACTUATION EXECUTED] Type: {act['type']} | Result: {act['result']}")

    print("\n[MOCK CITY BRAIN] Autonomous actuation demonstration complete.")
    print(f"Summary: Dispatches={brain.dispatches_sent}, Valves={brain.valve_commands_sent}, Signals={brain.signal_plans_sent}, Grids={brain.grid_switches_sent}")
