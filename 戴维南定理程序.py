from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


def simulate_original():
    """模拟含源二端网络接入负载的原电路。"""
    circuit = Circuit("Thevenin Original")

    # 12 V 电压源、R1=1 kΩ、R2=2 kΩ、负载 RL=3 kΩ
    circuit.V("s", "vin", circuit.gnd, 12 @ u_V)
    circuit.R(1, "vin", "a", 1 @ u_kΩ)
    circuit.R(2, "a", circuit.gnd, 2 @ u_kΩ)
    circuit.R("L", "a", circuit.gnd, 3 @ u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

    voltage = float(analysis["a"])
    current = voltage / 3000.0
    return voltage, current


def simulate_thevenin():
    """模拟戴维南等效电路接入同一负载。"""
    circuit = Circuit("Thevenin Equivalent")

    # U_th=8 V，R_th=R1||R2=666.6667 Ω
    circuit.V("th", "th_node", circuit.gnd, 8 @ u_V)
    circuit.R("th", "th_node", "a", 666.6667 @ u_Ω)
    circuit.R("L", "a", circuit.gnd, 3 @ u_kΩ)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.operating_point()

    voltage = float(analysis["a"])
    current = voltage / 3000.0
    return voltage, current


def main():
    original_voltage, original_current = simulate_original()
    equivalent_voltage, equivalent_current = simulate_thevenin()

    voltage_error = abs(original_voltage - equivalent_voltage) / original_voltage * 100
    current_error = abs(original_current - equivalent_current) / original_current * 100

    print("原电路：")
    print(f"负载电压 U_L = {original_voltage:.4f} V")
    print(f"负载电流 I_L = {original_current * 1000:.4f} mA")

    print("\n戴维南等效电路：")
    print(f"负载电压 U'_L = {equivalent_voltage:.4f} V")
    print(f"负载电流 I'_L = {equivalent_current * 1000:.4f} mA")

    print("\n验证结果：")
    print(f"电压相对误差 = {voltage_error:.6f}%")
    print(f"电流相对误差 = {current_error:.6f}%")


if __name__ == "__main__":
    main()
