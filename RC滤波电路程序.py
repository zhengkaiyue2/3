"""RC low-pass filter PySpice simulation."""
from pathlib import Path
import numpy as np
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
OUT = Path(__file__).with_name("results"); OUT.mkdir(exist_ok=True)
c = Circuit("RC low-pass")
c.SinusoidalVoltageSource("in", "in", c.gnd, amplitude=1 @ u_V, frequency=1 @ u_kHz)
c.R(1, "in", "out", 1 @ u_kOhm); c.C(1, "out", c.gnd, 100 @ u_nF)
sim = c.simulator(temperature=25, nominal_temperature=25)
tr = sim.transient(step_time=2 @ u_us, end_time=5 @ u_ms)
ac = sim.ac(start_frequency=10 @ u_Hz, stop_frequency=1 @ u_MHz, number_of_points=20, variation="dec")
np.savetxt(OUT / "rc_ac.csv", np.c_[np.array(ac.frequency), np.abs(np.array(ac.out))], delimiter=",", header="frequency_Hz,gain", comments="")
np.savetxt(OUT / "rc_transient.csv", np.c_[np.array(tr.time), np.array(tr.out)], delimiter=",", header="time_s,vout_V", comments="")
print("RC 截止频率: %.2f Hz" % (1 / (2 * np.pi * 1e3 * 100e-9)))
