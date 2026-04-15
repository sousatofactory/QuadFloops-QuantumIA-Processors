import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.visualization import circuit_drawer
import os
import sys

# Configurar encoding para o terminal
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- CONFIGURAÇÃO AOI XCAKE (ÂNCORA DE REALIDADE) ---
I_VAL, Q_VAL, N_VAL = 1.0, 1.0, -2.0
SIGMA_ANGLE = np.arccos(I_VAL / np.sqrt(I_VAL**2 + Q_VAL**2 + N_VAL**2))

def generate_iq9_higgs_circuit():
    qc = QuantumCircuit(4, name="IQ9_Higgs_Core")
    qc.h(range(4))
    qc.ry(SIGMA_ANGLE, [0, 1])
    qc.rz(N_VAL * np.pi, [2, 3])
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 0)
    qc.barrier()
    qc.u(1.1, 0, np.pi, 1)
    return qc

try:
    backend = GenericBackendV2(num_qubits=4, coupling_map=[[0,1], [1,2], [2,3], [3,0]])
    original_circuit = generate_iq9_higgs_circuit()
    transpiled_circuit = transpile(original_circuit, backend, optimization_level=3)

    print("--- [RELATÓRIO DE TRANSPILAÇÃO IQ/9 - SUCESSO] ---")
    print(f"Portas Originais: {original_circuit.count_ops()}")
    print(f"Portas Transpiladas (ISA QuadFloops): {transpiled_circuit.count_ops()}")
    print(f"Profundidade: {transpiled_circuit.depth()}")

    # Salvar em UTF-8 para evitar erros de codec
    scheme_text = str(circuit_drawer(transpiled_circuit, output='text'))
    with open(".gemini/iq9_circuit_scheme.txt", "w", encoding="utf-8") as f:
        f.write(scheme_text)

    print("\nCircuito salvo em '.gemini/iq9_circuit_scheme.txt' (UTF-8).")

except Exception as e:
    print(f"Erro na simulação: {e}")
