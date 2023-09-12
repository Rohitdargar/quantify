import cirq
from qramcircuits import bucket_brigade as bb
from qramcircuits.toffoli_decomposition import ToffoliDecompType
import random
import utils.misc_utils as miscutils
import pandas as pd



def main():

    n = 3
    # ones_indices = [0]

    address_qubits = [cirq.NamedQubit(f'adr_{i}') for i in range(n)]
    # target_qubit = cirq.NamedQubit('target')
    # memory = [cirq.NamedQubit("m" + miscutils.my_bin(i, n)) for i in range(2 ** (n))]



    # Create an initialization circuit
    # initialization_circuit = cirq.Circuit()

    # initialization_circuit.append(cirq.H(address_qubits[0]))
    # initialization_circuit.append(cirq.H(address_qubits[1]))
    # initialization_circuit.append(cirq.X(address_qubits[0]))
    # initialization_circuit.append(cirq.X(address_qubits[1]))

    # Initialize memory cells with data
    # m00 stays |0⟩ (no gate required)
    # initialization_circuit.append(cirq.X(memory[0]))  # m01 to |1⟩
    # initialization_circuit.append(cirq.X(memory[1]))  # m10 to |1⟩
    # initialization_circuit.append(cirq.X(memory[2]))
    # initialization_circuit.append(cirq.X(memory[3]))

    # m11 stays |0⟩ (no gate required)




    # Apply the X gate to qubits we want to initialize to |1⟩
    # for idx in ones_indices:
    #     initialization_circuit.append(cirq.X(address_qubits[idx]))


    decomp_scenario = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4_COMPUTE,  # fan_in_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4,  # mem_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_0_UNCOMPUTE,  # fan_out_decomp
        ],
        True
    )


    # bb_circuit = bb.BucketBrigade(address_qubits, decomp_scenario).construct_circuit(address_qubits, memory, target_qubit)

    bb_circuit = bb.BucketBrigade(address_qubits, decomp_scenario).construct_circuit(address_qubits)

    # print(bb_circuit)
    # bb_circuit.append(cirq.measure(target_qubit, key="ar"))

    # combined_circuit = initialization_circuit + bb_circuit
    # bb_circuit.append(cirq.measure(target_qubit, key="result"))

    # combined_circuit.append(cirq.X(target_qubit))

    print(bb_circuit)
    # combined_circuit.append(cirq.measure(target_qubit, key="rd"))

    # Simulate the circuit
    simulator = cirq.Simulator()
    results = simulator.run(bb_circuit, repetitions=1000)

    # Print the measurement outcomes
    print(results.histogram(key='r'))

    # bb_circuit.insert(0, cirq.X(address_qubits[0]))
    #
    # for qubit in address_qubits:
    #     bb_circuit.insert(1, cirq.H(qubit))
    #
    # bb_circuit.append(0, cirq.X(memory[0]))

    # bb_circuit.insert(0, cirq.X(memory[0]))
    # bb_circuit.insert(0, cirq.X(memory[1]))
    # bb_circuit.insert(0, cirq.X(memory[2]))
    # bb_circuit.insert(0, cirq.X(memory[3]))
    # bb_circuit.insert(0, cirq.H(target_qubit))



    # bb_circuit.append(cirq.measure(target_qubit, key='rs'))
    # print(bb_circuit)

    # bbqram = initialization_circuit + bb_circuit
    # print(bbqram)

    # Add measurements to the circuit
    # for qubit in address_qubits:
    #     bb_circuit.append(cirq.measure(qubit, key=qubit.name))


    # Simulate the circuit
    # simulator = cirq.Simulator()
    # rs = simulator.run(bb_circuit, repetitions=1000)
    #
    # # Print the measurement results
    # print(rs.histogram(key='rs'))

if __name__ == "__main__":
    main()
