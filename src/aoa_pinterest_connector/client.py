"""Bounded read-only client for Pinterest API v5."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from aoa_pinterest_connector import CONNECTOR_ID, __version__
from aoa_pinterest_connector.config import Credentials

API_BASE_URL = "https://api.pinterest.com/v5"
ACCOUNT_FIELDS = (
    "username",
    "account_type",
    "profile_image",
    "website_url",
    "business_name",
    "id",
)
PIN_FIELDS = (
    "id",
    "created_at",
    "link",
    "title",
    "description",
    "dominant_color",
    "alt_text",
    "board_id",
    "board_section_id",
    "board_owner",
    "media",
    "creative_type",
    "parent_pin_id",
    "is_owner",
)


class PinterestError(RuntimeError):
    """Base class for safe connector failures."""


class PinterestTransportError(PinterestError):
    """The API could not be reached or returned malformed transport data."""


@dataclass(frozen=True)
class PinterestAPIError(PinterestError):
    status: int | None
    code: int | None
    safe_message: str

    def __str__(self) -> str:
        parts = [self.safe_message]
        if self.code is not None:
            parts.append(f"code={self.code}")
        if self.status is not None:
            parts.append(f"http={self.status}")
        return "; ".join(parts)


class PinterestClient:
    def __init__(
        self,
        credentials: Credentials,
        *,
        timeout_seconds: float = 20.0,
        max_response_bytes: int = 2_000_000,
    ) -> None:
        self.credentials = credentials
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def get_account(self) -> dict[str, Any]:
        payload = self._get("user_account", {})
        if not payload.get("username"):
            raise PinterestTransportError("Pinterest user_account response lacked a username")
        return {
            field: payload[field]
            for field in ACCOUNT_FIELDS
            if field in payload and payload[field] is not None
        }

    def list_pins(self, *, page_size: int = 25, bookmark: str | None = None) -> dict[str, Any]:
        if not 1 <= page_size <= 250:
            raise ValueError("page size must be between 1 and 250")
        params = {"page_size": str(page_size)}
        if bookmark:
            params["bookmark"] = bookmark
        payload = self._get("pins", params)
        candidates = payload.get("items")
        if not isinstance(candidates, list):
            raise PinterestTransportError("Pinterest pins response lacked an items list")

        items: list[dict[str, Any]] = []
        for candidate in candidates:
            if not isinstance(candidate, dict) or not candidate.get("id"):
                continue
            items.append(
                {
                    field: candidate[field]
                    for field in PIN_FIELDS
                    if field in candidate and candidate[field] is not None
                }
            )
        next_bookmark = payload.get("bookmark")
        return {
            "items": items,
            "bookmark": str(next_bookmark) if next_bookmark else None,
        }

    def _get(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        query = f"?{urlencode(params)}" if params else ""
        request = Request(
            f"{API_BASE_URL}/{path}{query}",
            headers={
                "Authorization": f"Bearer {self.credentials.access_token}",
                "Accept": "application/json",
                "User-Agent": f"{CONNECTOR_ID}/{__version__}",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                status = getattr(response, "status", 200)
                body = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            body = exc.read(self.max_response_bytes + 1)
            payload = self._decode_json(body, allow_error=True)
            raise self._api_error(payload, status=exc.code) from None
        except (URLError, TimeoutError, OSError) as exc:
            raise PinterestTransportError(
                f"Pinterest API transport failed: {type(exc).__name__}"
            ) from None

        if len(body) > self.max_response_bytes:
            raise PinterestTransportError("Pinterest API response exceeded the size limit")
        payload = self._decode_json(body)
        if status >= 400 or "code" in payload and "message" in payload:
            raise self._api_error(payload, status=status)
        return payload

    def _decode_json(self, body: bytes, *, allow_error: bool = False) -> dict[str, Any]:
        if len(body) > self.max_response_bytes:
            raise PinterestTransportError("Pinterest API response exceeded the size limit")
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            if allow_error:
                return {}
            raise PinterestTransportError("Pinterest API returned invalid JSON") from None
        if not isinstance(payload, dict):
            raise PinterestTransportError("Pinterest API returned a non-object JSON response")
        return payload

    def _api_error(self, payload: dict[str, Any], *, status: int | None) -> PinterestAPIError:
        raw_message = str(payload.get("message") or "Pinterest API request failed")
        safe_message = raw_message.replace(self.credentials.access_token, "[redacted]")
        code = payload.get("code")
        return PinterestAPIError(
            status=status,
            code=code if isinstance(code, int) else None,
            safe_message=safe_message,
        )
