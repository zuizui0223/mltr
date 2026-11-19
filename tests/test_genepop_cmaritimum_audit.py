"""Zero-network unit tests: no synthetic genetic result is promoted as empirical."""
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_genepop_cmaritimum.py"
spec = importlib.util.spec_from_file_location("genepop_audit", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

TOY = b"""Synthetic-only diploid Genepop
Locus_A
Locus_B
Locus_C
POP
past1, 0102 0102 0000
past2, 0101 0101 0101
POP
current1, 0202 0101 0101
POP
exsitu1, 0101 0202 0101
"""


class GenepopAuditTests(unittest.TestCase):
    def test_strict_parse_and_qc(self):
        loci, pops = mod.parse_genepop(TOY)
        self.assertEqual((len(loci), len(pops), sum(map(len, pops))), (3, 3, 4))
        p = mod.profile(loci, pops[0])
        self.assertEqual(p["called_genotypes"], 5)
        self.assertEqual(p["call_fraction"], round(5 / 6, 8))
        self.assertEqual(p["observed_heterozygosity"], 0.4)

    def test_missing_map_keeps_history_unresolved(self):
        report = mod.analyse(TOY, {"mode": "test"})
        self.assertIsNone(report["historical_observed_allele_comparison"])
        self.assertEqual(report["status"], "POPULATION_QC_ONLY_NO_DECISION_RESPONSE")
        self.assertEqual(report["n_individuals"], 4)

    def test_explicit_map_counts_observed_alleles_not_extinction(self):
        report = mod.analyse(
            TOY, {"mode": "test"},
            {1: "past_wild", 2: "current_wild", 3: "ex_situ"},
        )
        comp = report["historical_observed_allele_comparison"]
        self.assertEqual(comp["past_observed_not_current_observed"], 2)
        self.assertEqual(comp["past_not_current_but_ex_situ_observed"], 2)
        self.assertEqual(comp["past_not_current_and_not_ex_situ_observed"], 0)
        self.assertEqual(comp["status"], "DESCRIPTIVE_SAMPLE_DETECTION_ONLY_NOT_ALLELE_EXTINCTION")

    def test_population_map_has_full_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "popmap.csv"
            path.write_text(
                "pop_index,group\n1,past_wild\n2,current_wild\n3,ex_situ\n", encoding="utf-8"
            )
            self.assertEqual(mod.read_map(path, 3)[1], "past_wild")
            path.write_text("pop_index,group\n1,past_wild\n3,ex_situ\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.read_map(path, 3)

    def test_malformed_and_partial_missing_are_rejected(self):
        for bad in [
            TOY.replace(b"0102 0102 0000", b"0102 0102"),
            TOY.replace(b"0102 0102 0000", b"0102 0002 0000"),
            TOY.replace(b"past2,", b"past1,"),
        ]:
            with self.subTest(bad=bad[:100]), self.assertRaises(ValueError):
                mod.parse_genepop(bad)

    def test_valid_three_digit_alleles(self):
        self.assertEqual(mod.allele_pair("001002"), ("001", "002"))
        self.assertIsNone(mod.allele_pair("000000"))
        with self.assertRaises(ValueError):
            mod.allele_pair("010")

    def test_archive_reader_has_no_uncontrolled_extract(self):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("one/Genepop_Cmaritimum.txt", TOY)
            z.writestr("one/README.txt", b"Synthetic test provenance")
        class DummyResponse:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, _):
                return archive.getvalue()
        with patch.object(mod.urllib.request, "urlopen", return_value=DummyResponse()):
            genepop, readme, provenance = mod.fetch_dryad()
        self.assertEqual(genepop, TOY)
        self.assertEqual(readme, b"Synthetic test provenance")
        self.assertEqual(provenance["doi"], mod.DOI)

    def test_public_metadata_file_stream_fallback(self):
        import hashlib
        import urllib.error

        dataset = {
            "identifier": "doi:" + mod.DOI,
            "_links": {"stash:version": {"href": "/api/v2/versions/813"}},
        }
        listing = {
            "_embedded": {"stash:files": [
                {"path": mod.TARGET, "id": 104, "size": len(TOY),
                 "digest": hashlib.sha256(TOY).hexdigest(), "digestType": "sha-256"},
                {"path": "README.txt", "id": 105, "size": 4},
            ]}
        }
        def public_get(url, _max):
            if url == mod.API_ZIP:
                raise urllib.error.HTTPError(url, 401, "Auth required", None, None)
            if url.endswith("/datasets/doi%3A10.5061%2Fdryad.tb2rbp03j"):
                return json.dumps(dataset).encode("utf-8")
            if "/versions/813/files" in url:
                return json.dumps(listing).encode("utf-8")
            if url.endswith("/file_stream/104"):
                return TOY
            if url.endswith("/file_stream/105"):
                return b"README"
            raise AssertionError(f"unreviewed URL: {url}")
        # README length mismatch deliberately asserted: no response is accepted silently.
        with patch.object(mod, "_fetch_bounded", side_effect=public_get):
            with self.assertRaises(ValueError):
                mod.fetch_dryad()
        listing["_embedded"]["stash:files"][1]["size"] = 6
        with patch.object(mod, "_fetch_bounded", side_effect=public_get):
            raw, readme, provenance = mod.fetch_dryad()
        self.assertEqual(raw, TOY)
        self.assertEqual(readme, b"README")
        self.assertEqual(provenance["version_id"], 813)
        self.assertEqual(provenance["genepop_file_id"], 104)

    def test_cli_emits_audited_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "original.gen"
            out = Path(tmp) / "report.json"
            raw.write_bytes(TOY)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(raw), "--out", str(out)],
                capture_output=True, text=True, check=True,
            )
            self.assertIn("POPULATION_QC_ONLY", result.stdout)
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(report["n_loci"], 3)
            self.assertEqual(report["historical_observed_allele_comparison"], None)


if __name__ == "__main__":
    unittest.main()
