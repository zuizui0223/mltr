# Arabidopsis seed analysis: production replay and claim audit

**Audit date: 2026-11-21. Status: unchanged production replay verified; original scientific conclusions retained.**

The merged seed entrypoint was executed locally on the two original, hash-pinned CSV files. Its aggregate output matches the committed result summary and the earlier independent calculation to the declared numerical tolerance. This supplies direct evidence that the production code processes the actual inputs; the earlier synthetic CI checks and separate implementations did not establish that by themselves.

## 1. What was verified

| Check | Observed result |
| --- | --- |
| Code baseline | `18ad4873780013b5fd283e615c596b38a108ed76`, the merged PR #50 commit |
| Retrieved source integrity | 25 repository files matched their Git blob SHA-1 identifiers, including all four analytical Python modules |
| Original fruit source | `full_data_drought.csv`, 21,391 bytes; SHA-256 `13ca229e6c97ee1a6d0333e4d32a66dabbf30a99e824a14c6f32bacad23067e3` |
| Original calibration source | `seed.count.drought.csv`, 519 bytes; SHA-256 `e85b41b6da29d8d505e01d0d3213d7a38f7a2e62fdb78071c70bbf6a8d31351d` |
| Production execution | Exit 0; 33 accessions, 659 prediction observations, 164 complete action panels |
| Committed summary comparison | 113 fields checked; no differences exceeding 1e-8; largest numeric difference 2.44e-9 |
| Earlier independent calculation comparison | 224 fields checked; no differences exceeding 1e-8; largest numeric difference approximately 1e-8 |
| Existing Arabidopsis tests | 26 passed, no failures or errors; synthetic inputs, assessed separately from original-data execution |
| Full existing project test suite | 107 tests and 2 subtests passed; includes the 26 Arabidopsis tests |

The comparisons cover source hashes and cohort counts in the committed summary, model MSEs, pooled and equal-accession gains, conditional intervals, fold and action summaries, policy choices and claim-gate outcomes. The four production prediction variants and primary raw-seed policy were checked. The earlier archive's additional exploratory sqrt-seed policy is outside this entrypoint and was not replayed. Free-text interpretation fields were reviewed rather than treated as numeric parity checks.

The 1e-8 absolute tolerance reflects the archived eight-decimal reporting precision. Very small summation or rounding differences are recorded in the audit; the gate decisions are unchanged. These are **337 field comparisons**, not 337 independent biological observations or new unit tests.

The first full-suite run exposed a local setup omission: the transport replay subprocess could not import the not-yet-installed project package. Installing the existing package in an isolated environment resolved that failure; the unchanged full suite then passed. An unrelated deprecation warning from the preinstalled test plugin remains. No analytical or theorem code was changed to make the tests pass.

## 2. Reproduced estimates and precise uncertainty targets

For prediction, gain is MSE(P1) minus MSE(P2), so positive values indicate lower fitted prediction error. P2c is centered within accession, using training cell frequencies. P2u is the older uncentered comparison.

| Endpoint | Pooled gain | Equal-accession gain | Conditional 95% interval for equal-accession gain | Frozen gate |
| --- | ---: | ---: | --- | --- |
| Raw estimated seeds, P2c prediction | 11,472.30002992 | 11,473.47070288 | [3,369.25562535, 20,154.48933222] | Fails: rack 5 gain −116.97195649 |
| Sqrt estimated seeds, P2c sensitivity | 2.29949935 | 2.30505979 | [0.44583184, 4.38812014] | Passes its exploratory numerical gate |
| Sqrt fruit, same33 sensitivity | 0.04125581 | 0.04131510 | [−0.00671095, 0.09615656] | Fails |
| Raw estimated-seed action choice | 5.64158537 per complete panel | 5.60739394 | [−77.81764394, 102.64908939] | Fails: interval crosses zero |

Prediction gains in each row use that row's squared-error scale and are not directly comparable across scales. The policy row is a difference in estimated seed output, not an MSE. All interval calculations first average within an accession, then resample those accession averages. The pooled row or panel average and equal-accession average differ slightly because one accession has one missing outcome/panel.

Prediction resampling uses seed `20261119`; policy resampling uses `20261120`; each uses 2,000 draws. These intervals are conditional descriptions with fitted predictions/policies and the supplied seed factors held fixed. They omit model-refitting and calibration uncertainty. Folds share training observations and are not independent replications.

The uncentered raw-seed gain is 20,199.07182938 and passes its numerical gate, but can partly repair the accession intercept. It is not substituted for the centered primary. The source protocol phrases the positive-mean condition as pooled MSE improvement; the inherited scorer checks the equal-accession mean sign. Both means are positive in all four reproduced prediction variants, so the protocol-based and implemented gate outcomes agree for these exact data. The replay audit records this distinction without revising the frozen protocol or thresholds.

## 3. What the evidence permits

The source records support a fitted prediction improvement whose robustness depends on response scale and held-out rack. They do not support promoting the primary raw-seed predictor to a uniformly favorable treatment-response claim. P2c changed the selected action in 23 of 164 panels, but the realized utility comparison supports neither benefit nor harm.

All 33 retained accession IDs occur in training and test racks. This is a known-accession block-holdout evaluation, not prediction for new genotypes, populations or lineages. The seed-per-fruit lookup comes from the same experiment, and the aggregate calibration table cannot establish rack-separated calibration. Five omitted accessions account for 64 zero-fruit records among 100 excluded design records, compared with 52 among 660 retained design cells; complete-calibration selection remains a material limitation.

The practical reporting decision therefore remains: **report the fitted, conditional prediction results with their scale and support restrictions; do not claim that accession-specific treatment selection improves seed production.** Computational reproducibility and scientific claim strength are separate assessments. No new genomic mechanism, causal genotype perturbation, independent biological replication, cost-aware field policy or exact MLTR theorem test is supplied by this replay.

The [application-gate synthesis](species_genomics_application_gate_2026-11-19.md) now includes this seed extension and distinguishes its known-accession evidence from the earlier out-of-lineage genomic-response proposal. The detailed seed report now labels the bootstrap target explicitly and describes the two source files as separately supplied files from one experiment. The original estimates, frozen protocol and analytical code are preserved.

## 4. Replay record and reproducibility

From the repository containing the unchanged analytical modules:

```bash
python3 scripts/audit_arabidopsis_original_seed_fitness.py \
  --fruit /path/to/full_data_drought.csv \
  --seed /path/to/seed.count.drought.csv \
  --out replay.json
python3 -m unittest discover -s tests -p 'test_arabidopsis_*.py' -v
```

The broader project suite requires the project package to be installed, as in CI:

```bash
python3 -m pip install -e '.[dev]'
python3 -m pytest -o addopts='' -q
```

The committed aggregate replay has SHA-256 `92fb419953dd12d264c61f56e5313efaf136d57057f827b7f0e973757e467140`. The audit identifies the analytical source blobs, input hashes, reference artifacts and every compared reference field. It records the comparison scope and maximum discrepancies rather than claiming that differently shaped JSON reports are byte-identical.

- [Unchanged production output](results/arabidopsis_original_seed_production_replay_2026-11-21.json)
- [Machine-readable replay audit](results/arabidopsis_seed_replay_audit_2026-11-21.json)
- [Earlier committed estimate summary](results/arabidopsis_original_seed_production_2026-11-20.json)
- [Detailed biological results and limitations](arabidopsis_original_seed_production_results_2026-11-20.md)

Original raw CSVs remain outside the repository. GitHub Actions does not receive them; the real-data verification recorded here was a local execution. This audit does not assert a second independent download or authentication of the Dryad bytes.
