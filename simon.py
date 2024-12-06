from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# Considering our bit string to be '101'
b = "101"
n = len(b)

# Creating two quantum registers of 'n' qubits and 1 classical register of 'n' qubits
q_reg1 = QuantumRegister(n, "reg1")
q_reg2 = QuantumRegister(n, "reg2")
c_reg = ClassicalRegister(n)
circuit = QuantumCircuit(q_reg1, q_reg2, c_reg)

# Applying H-gate on qubits of the first register
circuit.h(q_reg1)
circuit.barrier()

# Copying the data of the first register to the second register
circuit.cx(q_reg1, q_reg2)
circuit.barrier()

# Applying bitwise X-OR from register 1 to register 2 where qubits of the first register are 1
circuit.cx(q_reg1[0], q_reg2[0])
circuit.cx(q_reg1[0], q_reg2[2])
circuit.barrier()

# Measuring qubits of the second register
circuit.measure(q_reg2, c_reg)

# Applying H-gate to qubits of the first register
circuit.h(q_reg1)
circuit.barrier()

# Measuring qubits of the first register
circuit.measure(q_reg1, c_reg)

# Print the quantum circuit
print(circuit.draw())

# Running the circuit using the QASM simulator
qasm_sim = Aer.get_backend("qasm_simulator")

# Transpile the circuit for optimization and execution
transpiled_circuit = transpile(circuit, qasm_sim)

# Run the circuit directly without using 'assemble'
result = qasm_sim.run(transpiled_circuit, shots=1024).result()

# Get the counts (measurement results)
counts = result.get_counts()

# Define the bdotz function (dot product mod 2)
def bdotz(b, z):
    accum = 0
    for i in range(len(b)):
        accum += int(b[i]) * int(z[i])
    return (accum % 2)

# Iterate over the counts and print results using bdotz
for z in counts:
    print('{} . {} = {} (mod 2)'.format(b, z, bdotz(b, z)))

# Plot the histogram of the counts
plot_histogram(counts)

# Ensure the plot stays open
plt.show()
