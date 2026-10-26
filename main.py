"""Command-line entry point.

Examples
--------
python main.py                              # run both demonstration scenarios
python main.py --scenario crop_yield        # one scenario
python main.py --scenario crop_yield --data my_real_data.csv   # your own data (same schema)
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from agri_forecast.pipeline import run_scenario  # noqa: E402
from agri_forecast.plotting import plot_framework_diagram, plot_scenario_comparison  # noqa: E402
from agri_forecast.scenarios import SCENARIOS  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Agribusiness predictive modeling framework")
    ap.add_argument("--scenario", default="all", choices=["all", *SCENARIOS])
    ap.add_argument("--data", default=None, help="CSV with the scenario's schema (replaces synthetic data)")
    ap.add_argument("--out", default=str(ROOT / "results"))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n-iter", type=int, default=12, help="random-search iterations per model")
    ap.add_argument("--n-boot", type=int, default=2000, help="bootstrap replicates for CIs")
    args = ap.parse_args()

    if args.data and args.scenario == "all":
        ap.error("--data requires a specific --scenario")
    names = list(SCENARIOS) if args.scenario == "all" else [args.scenario]
    out = Path(args.out)
    (ROOT / "data").mkdir(exist_ok=True)
    summaries = {}
    for name in names:
        cfg, generator = SCENARIOS[name]
        raw = pd.read_csv(args.data) if args.data else generator(args.seed)
        if not args.data:
            raw.to_csv(ROOT / "data" / f"{name}_synthetic.csv", index=False)
        summaries[name] = run_scenario(cfg, raw, out, seed=args.seed, n_iter=args.n_iter, n_boot=args.n_boot)

    plot_framework_diagram(out / "framework_diagram.png")
    if len(summaries) > 1:
        plot_scenario_comparison(summaries, out / "scenario_comparison.png")
    with open(out / "all_summaries.json", "w") as f:
        json.dump(summaries, f, indent=2, default=str)
    print("\nFinished. Results in:", out)


if __name__ == "__main__":
    main()
