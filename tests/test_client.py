from __future__ import annotations

import json

import aoa_pinterest_connector.client as client_module
from aoa_pinterest_connector.client import PinterestClient
from aoa_pinterest_connector.config import Credentials


class FakeResponse:
    status = 200

    def __init__(self, payload: dict[str, object]) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def read(self, _limit: int) -> bytes:
        return self.body


def credentials() -> Credentials:
    return Credentials(access_token="pina_" + ("x" * 48), source_path=None)


def test_account_read_uses_bearer_header_not_query(monkeypatch) -> None:
    calls = []

    def fake_urlopen(request, *, timeout):
        calls.append((request, timeout))
        return FakeResponse({"username": "owned_account", "account_type": "BUSINESS", "id": "1"})

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    account = PinterestClient(credentials()).get_account()
    assert account["username"] == "owned_account"
    request, timeout = calls[0]
    assert "access_token" not in request.full_url
    assert request.get_header("Authorization").startswith("Bearer pina_")
    assert timeout == 20.0


def test_pin_read_is_bounded_and_drops_unknown_fields(monkeypatch) -> None:
    def fake_urlopen(request, *, timeout):
        assert "page_size=10" in request.full_url
        return FakeResponse(
            {
                "items": [{"id": "123", "title": "Example", "unexpected": "drop-me"}],
                "bookmark": "next-1",
            }
        )

    monkeypatch.setattr(client_module, "urlopen", fake_urlopen)
    page = PinterestClient(credentials()).list_pins(page_size=10)
    assert page["bookmark"] == "next-1"
    assert page["items"][0]["id"] == "123"
    assert "unexpected" not in page["items"][0]
