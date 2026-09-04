"""Normalize authorized Pinterest pins into AoA evidence packets."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from aoa_pinterest_connector import CONNECTOR_ID, PROVIDER


def evidence_page(
    account: dict[str, Any],
    pins_page: dict[str, Any],
    *,
    observed_at: str | None = None,
) -> dict[str, Any]:
    timestamp = observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    packets: list[dict[str, Any]] = []
    for pin in pins_page.get("items", []):
        if not isinstance(pin, dict) or not pin.get("id"):
            continue
        pin_id = quote(str(pin["id"]), safe="")
        packets.append(
            {
                "schema": "aoa_social_evidence_packet_v1",
                "provider": PROVIDER,
                "source_id": str(pin["id"]),
                "source_url": f"https://www.pinterest.com/pin/{pin_id}/",
                "observed_at": timestamp,
                "permission_basis": "pinterest_api_v5:pins:read",
                "payload": dict(pin),
            }
        )
    return {
        "schema": "aoa_social_evidence_page_v1",
        "connector_id": CONNECTOR_ID,
        "provider": PROVIDER,
        "observed_at": timestamp,
        "account": dict(account),
        "items": packets,
        "next_bookmark": pins_page.get("bookmark"),
        "network_effect": "read_only",
    }
