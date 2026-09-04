# Source Policy

Provider: Pinterest

Policy snapshot: 2026-09-04. Reverify all live conditions before adapter work.

## Planned official surfaces

- read: authorized_pins
- read: boards
- read: board_sections
- read: trends
- publication-plan target: image_pin
- publication-plan target: video_pin
- deferred: native_scheduling
- deferred: arbitrary_public_search

## Admission rules

- Official provider APIs and authorized accounts only.
- Every observation records source identity, time, URL, and permission basis.
- Account allowlists and topic allowlists are explicit configuration.
- Rate, quota, cost, retention, deletion, and review obligations fail closed.
- HTML scraping, session-cookie automation, CAPTCHA bypass, and stealth collection are out of scope.
- API success does not establish public visibility or consumer acceptance.

## Current provider boundary

The official API is strongest for authorized account assets and approved analytics/trends access. Scheduling is treated as an AoA runtime concern unless the current API explicitly provides it.

Official documentation: https://developers.pinterest.com/docs/api/v5/
