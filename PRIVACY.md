# Privacy Policy

Effective date: 2026-09-04

`aoa-pinterest-connector` is an operator-controlled connector developed under
the Agents of Abyss project. Its purpose is to help an authorized operator read,
organize, and prepare content from the Pinterest account that the operator
explicitly connects.

## Data handled

With the account holder's authorization, the connector may process the minimum
Pinterest account, board, Pin, media-metadata, and analytics fields required for
the enabled feature. The current Trial bootstrap is limited to the developer's
own authorized account and read-only account/Pin metadata.

The connector does not request a Pinterest password. OAuth access and refresh
tokens are secrets and are stored only in an operator-controlled secret store,
outside the public source repository.

## Use, retention, and sharing

Data is used only to provide the connector's requested retrieval, organization,
drafting, and explicitly approved publication functions. Data is not sold.
The connector does not share Pinterest data with third parties except the
infrastructure providers necessary to run the operator's own deployment.

The operator controls retention. Revoking Pinterest access stops new API access;
locally retained data can be removed from the operator-controlled deployment on
request. Public source code and test fixtures contain no account tokens or
private account exports.

## Contact and changes

Questions or deletion requests can be opened through the project's
[issue tracker](https://github.com/8Dionysus/aoa-pinterest-connector/issues/new).
Do not include passwords, tokens, or private account data in a public issue.

Material changes to this policy will be recorded in this repository with a new
effective date.
