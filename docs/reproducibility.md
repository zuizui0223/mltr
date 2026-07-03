# EXT reproducibility contract

## What is reproduced

The repository provides deterministic finite replays for:

1. a many-to-one replacement relation preserving one two-state macro-law;
2. construction of target labels from source labels and relation alone;
3. a target-only action that is uniformly portable within derived fibers;
4. a newly legal word that refutes one proposed carried merge;
5. a local target-only action split repaired by the coarsest relative exact refinement;
6. an accumulating binary family in which two source macrostates require
   \(2^m+1\) exact target macrostates after replacement;
7. a coherent replacement diamond with two routes, one carried partition, and one exact repair;
8. an incoherent boundary diamond with different root labels at terminal states; and
9. the minimum finite history contexts needed to retain those different carried maps.

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

The `Transport-core reproducibility` workflow runs transport, refinement, path,
and history tests, then uploads the JSON replay artifact. The artifact records
the Git commit SHA and Python version.

## Boundary between proof and replay

The tests and replay verify supplied finite systems, grammars, relations, and
witnesses. They do not automatically prove all finite-system theorems.

The manuscript must give independent symbolic proofs of:

- relation-preserving transport;
- derived target labels and exact target projection;
- conservative target-only action transport;
- local carried-fiber split obstruction;
- coarsest relative exact refinement;
- path-label coherence and route-independent repair; and
- minimum distinct-label-map history augmentation plus the exact repair of the
  resulting history-context system.

The replay is regression evidence and a reader-checkable finite realization of
those hypotheses and conclusions.
