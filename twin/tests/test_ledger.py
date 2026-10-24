"""Unit tests for Ground Truth SQLite Ledger (Phase 1)."""

import os
import tempfile
import pytest
from twin.db_ledger import (
    DeviceRecord,
    GroundTruthLedger,
    InjectedAttackRecord,
    TruthReadingRecord,
)


@pytest.fixture
def temp_db():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_ground_truth.db")
        yield db_path


def test_ledger_initialization(temp_db):
    ledger = GroundTruthLedger(db_path=temp_db)
    assert os.path.exists(temp_db)

    # Verify tables
    with ledger._get_connection() as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        ).fetchall()
        table_names = [t["name"] for t in tables]
        assert "devices" in table_names
        assert "readings_truth" in table_names
        assert "attacks_injected" in table_names


def test_device_registration_and_listing(temp_db):
    ledger = GroundTruthLedger(db_path=temp_db)
    device = DeviceRecord(
        device_id="dev-traffic-01",
        zone_id="zone-1",
        device_type="traffic_camera",
        unit="vehicles/min",
        lat=36.8065,
        lon=10.1815,
        public_key="test_pub_key_base64",
        status="ok",
        min_val=0.0,
        max_val=150.0,
    )
    ledger.register_device(device)

    dev = ledger.get_device("dev-traffic-01")
    assert dev is not None
    assert dev["device_id"] == "dev-traffic-01"
    assert dev["zone_id"] == "zone-1"
    assert dev["device_type"] == "traffic_camera"
    assert dev["unit"] == "vehicles/min"

    all_devices = ledger.list_devices()
    assert len(all_devices) == 1
    assert all_devices[0]["device_id"] == "dev-traffic-01"


def test_reading_truth_recording(temp_db):
    ledger = GroundTruthLedger(db_path=temp_db)
    device = DeviceRecord(
        device_id="dev-water-01",
        zone_id="zone-2",
        device_type="water_level",
        unit="meters",
        lat=36.8100,
        lon=10.1900,
        min_val=0.0,
        max_val=10.0,
    )
    ledger.register_device(device)

    reading = TruthReadingRecord(
        reading_id="read-001",
        device_id="dev-water-01",
        ts="2026-10-17T12:00:00Z",
        seq=1,
        true_value=3.45,
        broadcast_value=3.45,
        unit="meters",
        status="ok",
        sig="sig_base64_example",
        attack_type=None,
        is_attacked=False,
    )
    ledger.record_reading_truth(reading)

    fetched = ledger.get_reading_truth("read-001")
    assert fetched is not None
    assert fetched["reading_id"] == "read-001"
    assert fetched["device_id"] == "dev-water-01"
    assert fetched["true_value"] == 3.45
    assert fetched["broadcast_value"] == 3.45
    assert fetched["is_attacked"] == 0


def test_attack_injection_recording(temp_db):
    ledger = GroundTruthLedger(db_path=temp_db)
    attack = InjectedAttackRecord(
        attack_id="atk-001",
        capability="device_physical",
        target_device_id="dev-traffic-01",
        target_zone_id="zone-1",
        params_json='{"spoofed_value": 999.0}',
        start_sim_time="2026-10-17T12:00:00Z",
        end_sim_time=None,
        active=True,
        description="Physical sensor spoof test",
    )
    ledger.record_attack(attack)

    active_attacks = ledger.get_active_attacks()
    assert len(active_attacks) == 1
    assert active_attacks[0]["attack_id"] == "atk-001"
    assert active_attacks[0]["capability"] == "device_physical"
    assert active_attacks[0]["target_device_id"] == "dev-traffic-01"
