from __future__ import annotations

from aoa_pinterest_connector.evidence import evidence_page


def test_evidence_page_preserves_provenance() -> None:
    page = evidence_page(
        {"username": "owned_account", "id": "1"},
        {"items": [{"id": "123", "title": "Example"}], "bookmark": "next-1"},
        observed_at="2026-09-04T12:00:00Z",
    )
    assert page["network_effect"] == "read_only"
    assert page["next_bookmark"] == "next-1"
    packet = page["items"][0]
    assert packet["permission_basis"] == "pinterest_api_v5:pins:read"
    assert packet["source_url"] == "https://www.pinterest.com/pin/123/"
