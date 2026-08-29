import pandas as pd
import matplotlib.pyplot as mt
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

baseline_df = pd.read_csv(os.path.join(OUTPUTS_DIR, "results_baseline.csv"))
solar_df = pd.read_csv(os.path.join(OUTPUTS_DIR, "results_solar.csv"))
ev_df = pd.read_csv(os.path.join(OUTPUTS_DIR, "results_ev.csv"))

mt.figure(figsize=(12, 6))

mt.axhspan(0.94, 1.10, color="green", alpha=0.08, label="Safe operating band")

mt.plot(baseline_df["bus"], baseline_df["voltage_pu"], marker="o", label="Baseline (no solar/EV)")
mt.plot(solar_df["bus"], solar_df["voltage_pu"], marker="o", label="With solar at all houses")
mt.plot(ev_df["bus"], ev_df["voltage_pu"], marker="o", label="With EV chargers at all houses")

mt.axhline(y=0.94, color="red", linestyle="--", label="UK statutory lower limit (0.94pu)")
mt.axhline(y=1.10, color="orange", linestyle="--", label="UK statutory upper limit (1.10pu)")

solar_change = (solar_df["voltage_pu"].iloc[-1] - baseline_df["voltage_pu"].iloc[-1]) * 100
ev_change = (ev_df["voltage_pu"].iloc[-1] - baseline_df["voltage_pu"].iloc[-1]) * 100

mt.annotate(f"{solar_change:+.2f}%", xy=("bus6", solar_df["voltage_pu"].iloc[-1]),
             xytext=(5, 8), textcoords="offset points", color="orange", fontweight="bold")
mt.annotate(f"{ev_change:+.2f}%", xy=("bus6", ev_df["voltage_pu"].iloc[-1]),
             xytext=(5, -14), textcoords="offset points", color="green", fontweight="bold")

mt.ylim(0.93, 1.11)
mt.xlim(-0.5, len(baseline_df["bus"]) - 0.3)
mt.ylabel("Voltage (per unit)")
mt.xlabel("Bus (distance down the feeder)")
mt.title("Voltage Profile Comparison: Baseline vs Solar vs EV Chargers")
mt.legend(loc="upper right", fontsize=8)
mt.savefig(os.path.join(OUTPUTS_DIR, "voltage_profile_comparison.png"), dpi=350)
mt.show()