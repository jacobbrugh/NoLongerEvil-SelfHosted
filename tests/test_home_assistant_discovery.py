"""Tests for Home Assistant MQTT discovery payloads."""

from typing import Any

from nolongerevil.integrations.mqtt.home_assistant_discovery import get_all_discovery_configs

SERIAL = "02AA01AC3914096E"


def _configs() -> list[tuple[str, dict[str, Any]]]:
    return get_all_discovery_configs(
        SERIAL,
        device_values={},
        shared_values={"name": "Hallway", "target_temperature_type": "heat"},
        topic_prefix="nest",
    )


class TestEntityIdGeneration:
    """Home Assistant derives entity IDs from the device name, not the serial."""

    def test_no_payload_overrides_the_entity_id(self):
        """No payload sets default_entity_id or the deprecated object_id."""
        for topic, payload in _configs():
            assert "default_entity_id" not in payload, topic
            assert "object_id" not in payload, topic

    def test_climate_is_the_device_main_feature(self):
        """The climate entity is unnamed so HA names it after the device alone."""
        climate = next(payload for topic, payload in _configs() if "/climate/" in topic)
        assert climate["name"] is None
        assert climate["device"]["name"] == "Hallway"

    def test_unique_ids_keep_the_serial(self):
        """Registry identity stays per-thermostat even without serial-based entity IDs."""
        for topic, payload in _configs():
            assert SERIAL in payload["unique_id"], topic
