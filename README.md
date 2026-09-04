# aoa-pinterest-connector

Policy-gated Pinterest evidence and publication-plan connector for AoA.

Phase 0 is an offline, policy-first skeleton. It makes no live API calls,
contains no credentials, and cannot publish content.

## Owned here

- Pinterest-specific source policy and capability discovery
- normalized evidence-packet and publication-plan contracts
- provider-specific parsing, preparation, validation, and local decisions
- a fail-closed local CLI and repository validator

## Owned elsewhere

- cross-network campaign orchestration and editorial policy
- live MCP/HTTP composition, scheduling, queues, retries, and secret injection
- final publication authority and operator approval
- heavy captures, media, indexes, and generated corpora

## Current boundary

The official API is strongest for authorized account assets and approved analytics/trends access. Scheduling is treated as an AoA runtime concern unless the current API explicitly provides it.

Official documentation: https://developers.pinterest.com/docs/api/v5/

API terms, scopes, quotas, review requirements, and pricing can change. Recheck
the official documentation before implementing or admitting a live adapter.

## Bootstrap checks

```bash
python -m pip install -e ".[dev]"
python scripts/validate_connector.py
ruff check .
pytest
aoa-pinterest doctor --json
```

A green bootstrap proves only the source skeleton. It does not prove API access,
OAuth, deployment, publication, or consumer acceptance.
