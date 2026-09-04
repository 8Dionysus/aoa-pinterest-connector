# Boundaries

## Plane split

| Plane | Phase 0 state | Effect |
| --- | --- | --- |
| Evidence discovery/read | planned | read-only |
| Draft preparation | planned | no external effect |
| Publication plan | planned | no external effect |
| Publication commit | disabled | external write, approval required |

A publication plan is data, not permission. A successful API submission is not
the same claim as processing completion, public visibility, or consumer acceptance.

## Provider-specific admission

The official API is strongest for authorized account assets and approved analytics/trends access. Scheduling is treated as an AoA runtime concern unless the current API explicitly provides it.

## Data and privacy

- Collect only fields required by an admitted use case.
- Preserve source identity, observation time, URL, and permission basis.
- Apply current deletion, refresh, retention, and user-revocation duties.
- Store large or sensitive state outside Git under operator-owned paths.
