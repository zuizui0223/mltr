# EXT reproducibility contract

## What is reproduced

The repository provides deterministic finite replays for:

1. a many-to-one replacement relation preserving one two-state macro-law;
2. construction of target labels from source labels and relation alone;
3. a target-only action that is uniformly portable within derived fibers;
4. a newly legal word that refutes one proposed carried merge;
5. a local target-only action split repaired by the coarsest relative exact refinement; and
6. an accumulating binary family in which two source macrostates require
   \(2^m+1\) exact target macrostates after replacement.

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

The `Transport-core reproducibility` workflow runs both the transport and
relative-refinement test suites, then writes/uploads the JSON replay artifact.
The artifact includes the Git commit SHA and Python version.

## Boundary between proof and replay

The tests and replay verify the supplied finite systems, grammars, relations, and
witnesses. They do not prove the all-finite-system theorems automatically.

The manuscript must give independent symbolic proofs of:

- relation-preserving transport;
- well-defined derived target labels;
- exactness of the derived target projection;
- conservative target-only action transport;
- the local carried-fiber split obstruction; and
- coarsest relative exact refinement of a carried target partition.

The replay is regression evidence and a reader-checkable finite realization of
those hypotheses and conclusions.