#!/usr/bin/env python
"""CLI: python run_pipeline.py --scenario crop_yield [--data my.csv] [--n-iter 15]"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from agriyield.pipeline import run  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Agribusiness predictive modelling framework")
    ap.add_argument("--scenario", default="crop_yield", choices=["crop_yield", "dairy_milk", "all"])
    ap.add_argument("--data", default=None, help="optional CSV with the scenario schema (otherwise simulated)")
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--n-iter", type=int, default=15, help="random-search iterations per model")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    for s in (["crop_yield", "dairy_milk"] if a.scenario == "all" else [a.scenario]):
        run(s, a.out, a.data, a.n_iter, a.seed)
