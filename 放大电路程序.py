"""PySpice simulation of the NMOS common-source circuit."""
import numpy as np
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('NMOS common-source amplifier')
circuit.V('DD', 'vdd', circuit.gnd, 5@u_V)
circuit.V('in', 'inp', circuit.gnd, 'SIN(0 10m 1k) AC 1')
circuit.R('g1', 'vdd', 'g', 60@u_kOhm)
circuit.R('g2', 'g', circuit.gnd, 40@u_kOhm)
circuit.R('d', 'vdd', 'd', 2@u_kOhm)
circuit.C('b1', 'inp', 'g', 1@u_uF)
circuit.model('NM', 'NMOS', VTO=1, KP=0.8e-3, LAMBDA=0.02)
circuit.MOSFET(1, 'd', 'g', circuit.gnd, circuit.gnd, model='NM')

sim = circuit.simulator(temperature=25, nominal_temperature=25)
op = sim.operating_point()
vg = float(op.nodes['g']); vd = float(op.nodes['d'])
id_mA = abs(float(op.branches['vdd'])) * 1e3
print(f'OP: VGS={vg:.6f} V, ID={id_mA:.6f} mA, VDS={vd:.6f} V')
tran = sim.transient(step_time=1@u_us, end_time=5@u_ms)
vin = np.asarray(tran['inp']); vout = np.asarray(tran['d'])
print(f'TRAN: Vin_pp={vin.max()-vin.min():.6g} V, Vout_pp={vout.max()-vout.min():.6g} V')

if __name__ == '__main__':
    pass
