# EXT reproducibility contract

## What is reproduced

The repository provides deterministic finite replays for:

1. a many-to-one replacement relation preserving one two-state macro-law;
2. construction of target labels from source labels and relation alone;
3. a target-only action that is uniformly portable within derived fibers; and
4. a newly legal word that refutes one proposed carried merge.

Run locally:

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_transport_core.py --write-report
```

The replay creates:

```text
artifacts/transport_core_report.json
```

## GitHub Actions

The `Transport-core reproducibility` workflow performs the same test suite and
writes/uploads the JSON replay artifact. The artifact includes the Git commit SHA
and Python version.

## Boundary between proof and replay

The tests and replay verify the supplied finite systems, grammars, relations, and
witnesses. They do not prove the all-finite-system theorems automatically.

The manuscript must give independent symbolic proofs of:

- relation-preserving transport;
- well-defined derived target labels;
- exactness of the derived target projection;
- conservative target-only action transport; and
- the local carried-fiber split obstruction.

The replay is regression evidence and a reader-checkable finite realization of
those hypotheses and conclusions.
