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
        ]:
            with self.subTest(bad=bad[:100]), self.assertRaises(ValueError):
                mod.parse_genepop(bad)

    def test_repeated_population_code_is_not_duplicate_sample(self):
        repeated = TOY.replace(b"past2,", b"past1,")
        loci, pops = mod.parse_genepop(repeated)
        self.assertEqual(len(pops[0]), 2)
        self.assertEqual([name for name, genotypes in pops[0]], ["past1", "past1"])
        self.assertEqual(mod.analyse(repeated, {"mode": "test"})["duplicated_sample_ids_across_pop_blocks"], [])

    def test_source_readme_crosswalk_no_pop_order_assumptions(self):
        labels = ["C2", "C3", "C4", "C1-2", "C1-3", "C1-4", "C1-1"]
        spec = mod.SOURCE_LABELS
        lines = ["4. Sample information", "Cirsium maritimum"]
        for label, (site, year, ex_situ, _status) in spec.items():
            description = f"{label}: Collected in {site}, Japan, in {year}"
            if ex_situ:
                description += " and ex situ conserved at a garden"
            lines.append(description)
        lines.append("Linaria japonica")
        readme = ("\n".join(lines) + "\n").encode("utf-8")
        populations = []
        genepop_lines = ["Title line:Cirsium maritimum", "locus_a", "locus_b"]
        for label in labels:
            n = 2 if label == "C1-1" else 8
            genepop_lines.append("POP")
            row = "0102 0101" if label == "C1-1" else (
                "0202 0101" if label == "C1-2" else "0101 0101"
            )
            for row_index in range(n):
                # Source-like repeated population labels with distinct rows.
                genepop_lines.append(f"{label}, {row}" if row_index == 0 else (
                    f"{label}, {row if row_index % 2 == 0 else '0000 0101'}"
                ))
        genepop_raw = ("\n".join(genepop_lines) + "\n").encode("utf-8")
        # A population label is not a specimen ID. Identical genotype rows
        # may come from different real individuals and must be flagged, not deleted.
        _loci, parsed_pops = mod.parse_genepop(genepop_raw)
        self.assertEqual(sum(map(len, parsed_pops)), 50)
        scan = mod.analyse(genepop_raw, {"mode": "synthetic-test"})
        self.assertGreater(
            sum(x["repeated_genotype_rows"] for x in scan["identical_full_genotype_rows_within_pop_blocks"]), 0
        )
        # A smaller validated source-like hierarchy can still be tested
        # via README + genuine distinct rows without assuming POP order.
        populations = [
            [(label, [("01", "02"), ("01", "01")])]
            for label in labels
        ]
        self.assertEqual(mod.verify_source_labels(readme, populations), labels)
        changed = readme.replace(b"C1-1: Collected in Awaji Island, Japan, in 2007",
                                  b"C1-1: Collected in Awaji Island, Japan, in 2019")
        with self.assertRaises(ValueError):
            mod.verify_source_labels(changed, populations)

    def test_source_verified_real_format_analog_50_rows(self):
        expected = mod.SOURCE_LABELS
        labels = ["C2", "C3", "C4", "C1-2", "C1-3", "C1-4", "C1-1"]
        readme_lines = ["4. Sample information", "Cirsium maritimum"]
        for label, (site, year, ex_situ, _status) in expected.items():
            line = f"{label}: Collected in {site}, Japan, in {year}"
            if ex_situ:
                line += " and ex situ conserved at a garden"
            readme_lines.append(line)
        readme_lines.append("Linaria japonica")
        readme = ("\n".join(readme_lines) + "\n").encode("utf-8")
        loci = ["a", "b", "c"]
        genotype_lines = ["Title line:Cirsium maritimum"] + loci
        base_codes = ["0101", "0102", "0202", "0000"]
        for label in labels:
            n = 2 if label == "C1-1" else 8
            genotype_lines.append("POP")
            for i in range(n):
                first = ("0202" if label == "C1-2" else
                         "0102" if label == "C1-1" and i == 1 else "0101")
                genotype_lines.append(
                    f"{label}, {first} {base_codes[i%4]} {base_codes[i//4]}"
                )
        raw = ("\n".join(genotype_lines) + "\n").encode("utf-8")
        report = mod.source_verified_analysis(raw, readme, {"mode": "synthetic-test"})
        self.assertEqual(report["status"], "REAL_SOURCE_QC_COMPLETE_RESPONSE_LINK_MISSING")
        self.assertEqual((report["n_loci"], report["n_populations"], report["n_individuals"]), (3, 7, 50))
        self.assertEqual([x["sample_code"] for x in report["source_crosswalk"]], labels)
        self.assertEqual(report["observed_allele_contrasts"]["past_alleles_not_observed_current"], 1)
        self.assertEqual(report["observed_allele_contrasts"]["past_not_current_alleles_seen_in_one_past_individual"], 0)
        self.assertEqual(report["observed_allele_contrasts"]["past_not_current_observed_in_any_ex_situ"], 1)
        self.assertEqual(report["sample_size_and_missingness_sensitivity"]["n_comparisons_nonindependent"], 28)
        self.assertEqual(len(report["pairwise_genomic_differentiation"]["pairs"]), 15)
        self.assertTrue(all("fst" in item for item in report["pairwise_genomic_differentiation"]["pairs"]))
        self.assertFalse(report["duplicated_sample_ids_across_pop_blocks"])

    def test_hudson_fixed_opposite_and_identical_groups(self):
        a = [("x", [("01", "01"), ("01", "02")]) for _ in range(8)]
        b = [("x", [("02", "02"), ("01", "02")]) for _ in range(8)]
        result = mod.pairwise_hudson(a, b, 2, bootstrap_loci=50)
        self.assertGreater(result["fst"], 0.0)
        self.assertEqual(result["n_loci_pass_minimum_coverage"], 2)
        same = mod.pairwise_hudson(a, a, 2, bootstrap_loci=50)
        self.assertLess(same["fst"], 0.0)  # finite-sample correction
        self.assertGreaterEqual(len(result["leave_one_individual_each_population_fst_range"]), 2)

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
                {"path": mod.TARGET, "_links": {"self": {"href": "/api/v2/files/104"}}, "size": len(TOY),
                 "digest": hashlib.sha256(TOY).hexdigest(), "digestType": "sha-256"},
                {"path": "README.txt", "_links": {"self": {"href": "/api/v2/files/105"}}, "size": 4},
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
