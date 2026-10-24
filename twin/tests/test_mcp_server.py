"""Unit tests for Phase 4: MCP Command and Query Server Interface."""

import pytest
from twin.simulation import CitySimulator
from twin.mcp_server import (
    dispatch,
    get_city_state,
    get_command_result,
    get_device_key,
    get_device_state,
    get_reading,
    get_readings,
    isolate_device,
    list_devices,
    quarantine_device,
    reinstate_device,
    release_device,
    rollback_reading,
    set_active_simulator,
    set_signal_plan,
    set_valve,
    switch_grid,
)


@pytest.fixture(autouse=True)
def setup_simulator():
    sim = CitySimulator(seed=777)
    set_active_simulator(sim)
    yield sim


def test_mcp_list_devices(setup_simulator):
    devices = list_devices()
    assert len(devices) == 42
    for dev in devices:
        assert "device_id" in dev
        assert "min_val" in dev
        assert "max_val" in dev
        assert "unit" in dev

    # Test zone filter
    zone_1_devs = list_devices(zone_id="zone-1")
    assert len(zone_1_devs) == 7
    for d in zone_1_devs:
        assert d["zone_id"] == "zone-1"


def test_mcp_get_device_key(setup_simulator):
    sim = setup_simulator
    first_id = list(sim.devices.keys())[0]
    expected_pub_key = sim.devices[first_id].public_key

    pub_key = get_device_key(first_id)
    assert pub_key == expected_pub_key
    assert isinstance(pub_key, str) and len(pub_key) > 30


def test_mcp_get_device_state_and_city_state(setup_simulator):
    sim = setup_simulator
    first_id = list(sim.devices.keys())[0]

    state = get_device_state(first_id)
    assert state is not None
    assert state["device_id"] == first_id
    assert "current_value" in state
    assert state["status"] == "ok"

    city_state = get_city_state()
    assert city_state["total_devices"] == 42
    assert len(city_state["zones"]) == 6


def test_mcp_actuation_tools(setup_simulator):
    sim = setup_simulator

    # 1. Dispatch
    disp_res = dispatch(incident_type="flood_warning", zone_id="zone-1", idempotency_key="cmd-001")
    assert disp_res["status"] == "ok"
    assert disp_res["zone_id"] == "zone-1"
    assert get_command_result("cmd-001") == disp_res

    # 2. Set signal plan
    traffic_dev = "z1-tc1"
    plan_res = set_signal_plan(traffic_dev, "green_wave", idempotency_key="cmd-002")
    assert plan_res["status"] == "ok"
    assert sim.devices[traffic_dev].actuator_state["signal_plan"] == "green_wave"
    assert get_command_result("cmd-002") == plan_res

    # 3. Set valve
    water_dev = "z1-wl1"
    valve_res = set_valve(water_dev, "open", idempotency_key="cmd-003")
    assert valve_res["status"] == "ok"
    assert sim.devices[water_dev].actuator_state["valve_position"] == "open"
    assert get_command_result("cmd-003") == valve_res

    # 4. Switch grid
    power_dev = "z1-pl1"
    grid_res = switch_grid(power_dev, "grid_b", idempotency_key="cmd-004")
    assert grid_res["status"] == "ok"
    assert sim.devices[power_dev].actuator_state["grid_state"] == "grid_b"
    assert get_command_result("cmd-004") == grid_res


def test_mcp_containment_tools(setup_simulator):
    sim = setup_simulator
    target_dev = "z2-tc1"

    # Isolate
    iso_res = isolate_device(target_dev)
    assert iso_res["status"] == "ok"
    assert sim.devices[target_dev].status == "isolated"

    # Quarantine
    quar_res = quarantine_device(target_dev)
    assert quar_res["status"] == "ok"
    assert sim.devices[target_dev].status == "quarantined"

    # Reinstate
    rein_res = reinstate_device(target_dev)
    assert rein_res["status"] == "ok"
    assert sim.devices[target_dev].status == "ok"

    # Release
    quarantine_device(target_dev)
    rel_res = release_device(target_dev)
    assert rel_res["status"] == "ok"
    assert sim.devices[target_dev].status == "ok"


def test_mcp_reading_retrieval_and_rollback(setup_simulator):
    sim = setup_simulator
    readings = sim.tick()
    assert len(readings) == 42
    sample_reading = readings[0]
    rid = sample_reading["reading_id"]

    fetched = get_reading(rid)
    assert fetched is not None
    assert fetched["reading_id"] == rid

    all_recent = get_readings(limit=10)
    assert len(all_recent) == 10

    # Rollback reading
    rb_res = rollback_reading(rid)
    assert rb_res["status"] == "ok"
    updated = get_reading(rid)
    assert updated["status"] == "rolled_back"


def test_mcp_isolation_from_ground_truth_ledger():
    """Verify that MCP server module has no import or direct reference to GroundTruthLedger."""
    import twin.mcp_server as mcp_mod
    assert not hasattr(mcp_mod, "GroundTruthLedger")
    assert not hasattr(mcp_mod, "db_ledger")
