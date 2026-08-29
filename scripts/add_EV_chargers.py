import py_dss_interface
import pandas as pd
import matplotlib.pyplot as mt
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

dss = py_dss_interface.DSS()
dss.text("clear")

dss.text("new circuit.UK_LV_Feeder basekv=11 pu=1.0 phases=3 bus1=sourcebus")

dss.text("new transformer.T1 phases=3 windings=2 "
         "buses=(sourcebus, bus1) conns=(delta, wye) "
         "kvs=(11, 0.415) kvas=(100, 100) xhl=4")

dss.text("new linecode.LVcable nphases=3 r1=0.253 x1=0.0715 "
         "r0=0.44 x0=0.196 units=km")

houses = ["bus2", "bus3", "bus4", "bus5", "bus6"]
previous_bus = "bus1"
for i, house_bus in enumerate(houses, start=1):
    dss.text(f"new line.L{i} bus1={previous_bus} bus2={house_bus} "
              f"linecode=LVcable length=0.05 units=km phases=3")
    previous_bus = house_bus

for i, house_bus in enumerate(houses, start=1):
    dss.text(f"new load.House{i} bus1={house_bus} phases=3 conn=wye "
              f"kv=0.415 kw=3 pf=0.95 model=1")

for i, house_bus in enumerate(houses, start=1):
    dss.text(f"new load.EV{i} bus1={house_bus} phases=3 conn=wye "
              f"kv=0.415 kw=7 pf=0.98 model=1")

dss.text("set voltagebases=[11, 0.415]")
dss.text("calcvoltagebases")
dss.text("solve")

results = []
for bus_name in dss.circuit.buses_names:
    dss.circuit.set_active_bus(bus_name)
    voltages_pu = dss.bus.vmag_angle_pu
    magnitudes_only = voltages_pu[0::2]
    avg_voltage_pu = sum(magnitudes_only) / len(magnitudes_only)
    results.append({"bus": bus_name, "voltage_pu": avg_voltage_pu})

df = pd.DataFrame(results)
print(df)
df.to_csv(os.path.join(OUTPUTS_DIR, "results_ev.csv"), index=False)

mt.plot(df["bus"], df["voltage_pu"], marker="o", label="With EV chargers at all houses")
mt.axhline(y=0.94, color="red", linestyle="--", label="UK statutory lower limit (0.94pu)")
mt.axhline(y=1.10, color="orange", linestyle="--", label="UK statutory upper limit (1.10pu)")
mt.ylabel("Voltage (per unit)")
mt.xlabel("Bus (distance down the feeder)")
mt.title("Voltage Profile With EV Chargers at Every House")
mt.legend()
mt.savefig(os.path.join(OUTPUTS_DIR, "voltage_profile_with_ev.png"), dpi=350)
mt.show()