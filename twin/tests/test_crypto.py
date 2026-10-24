"""Unit tests for Ed25519 Cryptographic Utilities."""

from twin.crypto_utils import (
    canonicalize_for_signing,
    generate_keypair,
    sign_payload,
    verify_payload_signature,
)


def test_keypair_generation():
    priv, pub = generate_keypair()
    assert isinstance(priv, str) and len(priv) > 0
    assert isinstance(pub, str) and len(pub) > 0
    assert priv != pub


def test_payload_signing_and_verification():
    priv, pub = generate_keypair()
    payload = {
        "reading_id": "test-read-01",
        "device_id": "dev-01",
        "device_type": "water_level",
        "ts": "2026-10-17T12:00:00Z",
        "seq": 42,
        "value": 12.34,
        "unit": "meters",
        "location": {"zone_id": "zone-1", "lat": 36.8, "lon": 10.1},
        "status": "ok",
    }

    sig = sign_payload(payload, priv)
    assert isinstance(sig, str) and len(sig) > 0

    payload_with_sig = dict(payload)
    payload_with_sig["sig"] = sig

    assert verify_payload_signature(payload_with_sig, pub) is True

    # Tampered payload fails
    tampered_payload = dict(payload_with_sig)
    tampered_payload["value"] = 99.99
    assert verify_payload_signature(tampered_payload, pub) is False

    # Wrong public key fails
    _, other_pub = generate_keypair()
    assert verify_payload_signature(payload_with_sig, other_pub) is False
