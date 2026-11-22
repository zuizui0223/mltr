"""Synthetic leakage, action-ranking and conditional-uncertainty checks.

No original experimental genotype/fitness rows are embedded. NumPy is optional
to the theorem-only CI but required for the dedicated empirical workflow.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    import numpy as np
except ImportError:
    raise unittest.SkipTest("NumPy required only in dedicated Exposito empirical CI")

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/"scripts"
sys.path.insert(0,str(SCRIPTS))
SOURCE=SCRIPTS/"audit_exposito_rainfall_decision.py"
spec=importlib.util.spec_from_file_location("exposito_rainfall_decision",SOURCE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def toy_arrays(n=20):
    ids=np.array([str(i+1) for i in range(n)])
    # All eight combinations have published-type positive/zero outcomes.
    # Each accession has an increasing high-rainfall treatment benefit.
    fitness=np.zeros((n,8),dtype=float)
    for j in range(n):
        for _,h,l in m.STRATA:
            hi=m.CONTEXTS.index(h);li=m.CONTEXTS.index(l)
            fitness[j,li]=10.0
            fitness[j,hi]=10.0+(j+1)
    coords=np.column_stack((np.linspace(-45.,45.,n),np.linspace(-85.,85.,n)))
    d=np.abs(np.arange(n)[:,None]-np.arange(n)[None,:]).astype(float)/n
    return {"ids":ids,"coords":coords,"distance":d,"fitness":fitness,
            "contexts":np.asarray(m.CONTEXTS)}


def stub_fitter_checked(log):
    def _fit(data,train,held,mode,fold_index):
        # No held-out target is visible to fitting/tuning.
        assert np.isnan(data["fitness"][held]).all()
        assert np.isfinite(data["fitness"][train]).all()
        assert len(set(train)&set(held))==0
        # Mean normalization deliberately changes high-vs-low magnitude:
        # these are dimensionless predictions and MUST be rescaled.
        means=np.array([3.,1.,3.,1.,3.,1.,3.,1.])
        p0=np.ones((len(held),8),dtype=float)
        p1=np.ones_like(p0)
        numeric=np.asarray(data["ids"][held],dtype=int)
        for _,high,low in m.STRATA:
            hi=m.CONTEXTS.index(high);li=m.CONTEXTS.index(low)
            p0[:,hi]=1.0;p0[:,li]=1.0
            p1[:,hi]=1.+numeric/100.;p1[:,li]=1.0
        log.append({"train":len(train),"test":len(held),"mode":mode,
                    "fit_index":fold_index})
        return {"predictions":{"M0":p0,"M1":p1},
                "training_means":means,
                "selected_lambdas":{"M0":.1,"M1":1.0}}
    return _fit


class RainfallChoiceTests(unittest.TestCase):
    def test_positive_numeric_ids_and_ties_obey_quota(self):
        chosen=m.choose_high_rainfall(["9","2","11","1"],
                                      [2.,2.,2.,2.],[1.,1.,1.,1.])
        self.assertEqual(chosen.tolist(),[False,False,False,True])
        five=m.choose_high_rainfall(["5","4","3","2","1"],
                                    [1.,1.,1.,1.,1.],[1.,1.,1.,1.,1.])
        self.assertEqual(int(five.sum()),2)
        self.assertEqual(np.flatnonzero(five).tolist(),[3,4])

    def test_unknown_or_nonfinite_predictors_refused(self):
        for ids,high,low in [
            (["1","1"],[1.,2.],[0.,0.]),
            (["1","0"],[1.,2.],[0.,0.]),
            (["1","2"],[np.nan,2.],[0.,0.]),
            (["1","2"],[-1.,2.],[0.,0.]),
            (["1","2"],[1.],[0.,0.]),
        ]:
            with self.subTest(ids=ids),self.assertRaises(ValueError):
                m.choose_high_rainfall(ids,high,low)

    def test_two_equal_budget_policies_can_have_positive_value(self):
        ids=np.array(["1","2","3","4"])
        raw=np.zeros((4,8))
        m0=np.zeros((4,8));m1=np.zeros((4,8))
        for _,h,l in m.STRATA:
            hi=m.CONTEXTS.index(h);li=m.CONTEXTS.index(l)
            raw[:,hi]=[1.,2.,3.,4.]
            raw[:,li]=0.
            m0[:,hi]=1.
            m1[:,hi]=[1.,2.,3.,4.]
        difference,strata,changes=m.evaluate_heldout_policy(
            ids,raw,{"M0":m0,"M1":m1})
        self.assertAlmostEqual(float(difference.mean()),.75)
        self.assertEqual(changes,8)
        self.assertTrue(all(x["high_rainfall_quota"]==1 for x in strata))
        self.assertTrue(all(x["n_changed_accession_rainfall_decisions"]==2 for x in strata))

    def test_identical_actions_have_exact_zero_value(self):
        ids=np.array(["1","2","3","4"])
        raw=np.ones((4,8))
        pred=np.ones((4,8))
        v,_,changes=m.evaluate_heldout_policy(ids,raw,{"M0":pred,"M1":pred})
        self.assertEqual(changes,0)
        self.assertTrue(np.array_equal(v,np.zeros((4,4))))

    def test_predicted_policy_never_sees_heldout_fitness(self):
        source=toy_arrays(514)
        cohort_sha=hashlib.sha256(("\n".join(source["ids"])+"\n").encode()).hexdigest()
        log=[]
        with mock.patch.object(m,"COHORT_IDS_SHA256",cohort_sha):
            result=m.evaluate_policy(source,"accession",fit_function=stub_fitter_checked(log))
        self.assertEqual(len(log),5)
        self.assertEqual(result["n_site_density_decisions"],514*4)
        self.assertTrue(result["numerical_gate"]["passed"])
        self.assertGreater(result["M1_minus_M0_mean_realized_estimated_fitness"],0)
        self.assertGreater(result["n_changed_accession_stratum_decisions"],0)
        self.assertEqual(len(result["folds"]),5)

    def test_geographic_folds_keep_cells_together_and_mask_outcomes(self):
        source=toy_arrays(514)
        cohort_sha=hashlib.sha256(("\n".join(source["ids"])+"\n").encode()).hexdigest()
        log=[]
        with mock.patch.object(m,"COHORT_IDS_SHA256",cohort_sha):
            result=m.evaluate_policy(source,"geographic",fit_function=stub_fitter_checked(log))
        self.assertEqual(result["n_site_density_decisions"],514*4)
        self.assertEqual(result["split"],"geographic")
        self.assertEqual(len(log),5)
        self.assertEqual(result["conditional_interval"]["unit"],"five_degree_origin_cell")

    def test_bootstrap_accession_and_geographic_unit_accounting(self):
        gain=np.array([10.,10.,-3.,-3.])
        acc=m.conditional_interval(gain)
        grouped=m.conditional_interval(gain,np.array([[1,2],[1,2],[3,4],[3,4]]))
        self.assertEqual(acc["resampling_clusters"],4)
        self.assertEqual(grouped["resampling_clusters"],2)
        self.assertAlmostEqual(acc["mean"],3.5)
        self.assertAlmostEqual(grouped["mean"],3.5)
        self.assertEqual(m.conditional_interval(gain),acc)

    def test_validation_blocks_negative_outcome_and_wrong_contexts(self):
        ids=np.array(["1","2","3","4"])
        observed=np.zeros((4,8));pred=np.ones_like(observed)
        observed[0,2]=-1.
        with self.assertRaisesRegex(ValueError,"heldout fitness"):
            m.evaluate_heldout_policy(ids,observed,{"M0":pred,"M1":pred})
        with self.assertRaisesRegex(ValueError,"only frozen"):
            m.evaluate_heldout_policy(ids,np.ones((4,8)),{"M0":pred,"M2":pred})

    def test_protocol_source_hash_is_locked(self):
        path=ROOT/"docs"/"exposito_rainfall_decision_protocol_2026-11-22.md"
        self.assertEqual(m.git_blob_sha1(path.read_bytes()),m.PROTOCOL_GIT_BLOB_SHA1)
        with tempfile.TemporaryDirectory() as tmp:
            forged=Path(tmp)/"altered.md"
            forged.write_bytes(path.read_bytes()+b"\n")
            self.assertNotEqual(m.git_blob_sha1(forged.read_bytes()),m.PROTOCOL_GIT_BLOB_SHA1)

    def test_outcome_denormalization_affects_rainfall_selection(self):
        # In relative units, genotype "4" has the largest h-l gap; in raw
        # units genotype "1" has the largest gap due to the high-rainfall
        # training-mean multiplier. Catch inadvertently ranking normalized y.
        ids=np.array(["1","2","3","4"])
        h=np.array([2.0,1.95,1.9,1.85])
        l=np.array([3.0,2.9,2.8,2.7])
        rel=m.choose_high_rainfall(ids,h,l)
        raw=m.choose_high_rainfall(ids,10*h,1*l)
        self.assertNotEqual(np.flatnonzero(rel).tolist(),np.flatnonzero(raw).tolist())
        self.assertEqual(np.flatnonzero(raw).tolist(),[0])


if __name__=="__main__":
    unittest.main()
