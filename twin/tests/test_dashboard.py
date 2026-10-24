"""Unit and Integration Tests for Dashboard and Adversary Console (Layer 1).

Assigned to: Agent_QA
Tests:
1. Read-only SQLite isolation for the Dashboard.
2. Scoreboard metric aggregation and truth ledger retrieval.
3. Internal REST API routes on starlette_app (/api/status, /api/attack/inject, /api/attack/clear, /api/attack/active).
4. Threat injection and clearing routines across capabilities.
"""

import os
import sqlite3
import pytest
from starlette.testclient import TestClient

from twin.db_ledger import GroundTruthLedger, TruthReadingRecord, InjectedAttackRecord
from twin.simulation import CitySimulator
from twin.mcp_server import mcp, set_active_simulator
import dashboard


@pytest.fixture
def test_sim_and_db(tmp_path):
    """Create isolated GroundTruthLedger and CitySimulator in tmp directory."""
    db_path = str(tmp_path / "test_truth.db")
    ledger = GroundTruthLedger(db_path=db_path)
    sim = CitySimulator(seed=123, ledger=ledger)
    set_active_simulator(sim)

    # Populate sample readings
    sim.tick()
    sim.tick()

    # Inject one sample attack
    sim.inject_attack(
        capability="device_physical",
        target_device_id="z1-tc1",
        params={"spoofed_value": 180.0},
        description="Test physical attack",
    )
    sim.tick()

    return sim, ledger, db_path


def test_dashboard_read_only_isolation(test_sim_and_db, monkeypatch):
    """Verify that dashboard functions connect strictly in read-only mode."""
    sim, ledger, db_path = test_sim_and_db
    monkeypatch.setattr(dashboard, "DB_PATH", db_path)

    # Scoreboard metrics should reflect populated data
    metrics = dashboard.fetch_scoreboard_metrics()
    assert metrics["total_readings"] > 0
    assert metrics["active_attacks"] == 1
    assert metrics["active_incidents"] > 0
    assert "Z" in metrics["latest_sim_time"]

    # Truth ledger retrieval
    df = dashboard.fetch_truth_ledger(limit=10)
    assert not df.empty
    assert "true_value" in df.columns
    assert "broadcast_value" in df.columns
    assert "is_attacked" in df.columns

    # Active attacks
    active = dashboard.fetch_active_attacks()
    assert len(active) == 1
    assert active[0]["capability"] == "device_physical"

    # Timeline events
    timeline = dashboard.fetch_timeline_events(limit=10)
    assert len(timeline) > 0

    # Ensure a write query using dashboard's read-only connection is rejected
    conn = dashboard.get_db_connection()
    assert conn is not None
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("INSERT INTO readings_truth (reading_id, device_id, ts, seq, true_value, broadcast_value, unit, status, created_at_wall_clock) VALUES ('bad', 'bad', 'bad', 1, 0, 0, 'u', 'ok', 'now')")
    conn.close()


def test_starlette_internal_attack_api(test_sim_and_db):
    """Test the internal REST endpoints added to starlette_app."""
    sim, ledger, db_path = test_sim_and_db

    # Build starlette app matching twin.main
    starlette_app = mcp.sse_app(host="0.0.0.0")

    from starlette.requests import Request
    from starlette.responses import JSONResponse

    async def api_status(request: Request) -> JSONResponse:
        return JSONResponse({
            "status": "ok",
            "sim_time": sim.get_sim_time(),
            "tick_count": sim.clock.tick_count,
            "total_devices": len(sim.devices),
            "active_attacks_count": len(sim.active_attacks),
        })

    async def api_inject_attack(request: Request) -> JSONResponse:
        body = await request.json()
        aid = sim.inject_attack(
            capability=body["capability"],
            target_device_id=body.get("target_device_id"),
            target_zone_id=body.get("target_zone_id"),
            params=body.get("params", {}),
            description=body.get("description"),
        )
        return JSONResponse({"status": "ok", "attack_id": aid})

    async def api_clear_attack(request: Request) -> JSONResponse:
        body = await request.json() if request.headers.get("content-length") not in (None, "0") else {}
        attack_id = body.get("attack_id")
        if attack_id and attack_id != "all":
            cleared = sim.clear_attack(attack_id)
            return JSONResponse({"status": "ok", "cleared": cleared})
        else:
            sim.clear_all_attacks()
            return JSONResponse({"status": "ok", "cleared_all": True})

    async def api_active_attacks(request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok", "active_attacks": list(sim.active_attacks.values())})

    starlette_app.add_route("/api/status", api_status, methods=["GET"])
    starlette_app.add_route("/api/attack/inject", api_inject_attack, methods=["POST"])
    starlette_app.add_route("/api/attack/clear", api_clear_attack, methods=["POST"])
    starlette_app.add_route("/api/attack/active", api_active_attacks, methods=["GET"])

    client = TestClient(starlette_app)

    # 1. Test status
    res = client.get("/api/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["total_devices"] == 42

    # 2. Test inject attack
    inject_res = client.post(
        "/api/attack/inject",
        json={
            "capability": "sensor_fault",
            "target_device_id": "z2-wl1",
            "params": {"fault_mode": "drift", "drift_rate": 2.0},
            "description": "Test drift attack via API",
        },
    )
    assert inject_res.status_code == 200
    aid = inject_res.json()["attack_id"]
    assert aid.startswith("atk-")
    assert "z2-wl1" in sim.devices
    assert sim.devices["z2-wl1"].active_attack is not None

    # 3. Test active attacks list
    active_res = client.get("/api/attack/active")
    assert active_res.status_code == 200
    assert len(active_res.json()["active_attacks"]) >= 2

    # 4. Test clear specific attack
    clear_res = client.post("/api/attack/clear", json={"attack_id": aid})
    assert clear_res.status_code == 200
    assert clear_res.json()["cleared"] is True

    # 5. Test clear all attacks
    clear_all_res = client.post("/api/attack/clear", json={"attack_id": "all"})
    assert clear_all_res.status_code == 200
    assert len(sim.active_attacks) == 0


def test_dashboard_injection_interfacing(test_sim_and_db, monkeypatch):
    """Test dashboard.inject_attack_to_simulator and clear_attacks_in_simulator."""
    sim, ledger, db_path = test_sim_and_db
    monkeypatch.setattr(dashboard, "DB_PATH", db_path)

    # In local testing without mock server, direct Python singleton binding takes over
    success, msg = dashboard.inject_attack_to_simulator(
        capability="link",
        target_device_id="z3-pl1",
        params={"link_mode": "corrupt_bytes"},
        description="Dashboard test link attack",
    )
    assert success is True
    assert "z3-pl1" in sim.devices
    assert sim.devices["z3-pl1"].active_attack is not None

    # Clear attacks
    success_clear, clear_msg = dashboard.clear_attacks_in_simulator()
    assert success_clear is True
    assert len(sim.active_attacks) == 0


def test_dashboard_geospatial_and_divergence(test_sim_and_db, monkeypatch):
    """Test 3D geospatial sensor queries, neighborhood summaries, and time-series divergence."""
    sim, ledger, db_path = test_sim_and_db
    monkeypatch.setattr(dashboard, "DB_PATH", db_path)

    # 1. Test geospatial sensors query
    sensors_df = dashboard.fetch_geospatial_sensors()
    assert not sensors_df.empty
    assert "lat" in sensors_df.columns
    assert "lon" in sensors_df.columns
    assert "zone_name" in sensors_df.columns
    assert "discrepancy" in sensors_df.columns
    assert len(sensors_df) == 42

    # Check that z1-tc1 was marked as an active attack from fixture
    z1_tc1 = sensors_df[sensors_df["device_id"] == "z1-tc1"]
    assert not z1_tc1.empty
    assert bool(z1_tc1["discrepancy"].iloc[0]) is True
    assert z1_tc1["attack_type"].iloc[0] == "device_physical"

    # 2. Test neighborhood summaries
    summaries = dashboard.fetch_neighborhood_summaries(sensors_df)
    assert len(summaries) == 6
    zone1_sum = next(s for s in summaries if s["zone_id"] == "zone-1")
    assert zone1_sum["active_threats"] >= 1
    assert zone1_sum["status"] == "threat"
    assert zone1_sum["total_sensors"] == 7

    # 3. Test device time series divergence
    ts_df = dashboard.fetch_device_time_series("z1-tc1", limit=10)
    assert not ts_df.empty
    assert "true_value" in ts_df.columns
    assert "broadcast_value" in ts_df.columns
    assert "discrepancy" in ts_df.columns
    assert (ts_df["broadcast_value"] - ts_df["true_value"]).abs().max() > 0

