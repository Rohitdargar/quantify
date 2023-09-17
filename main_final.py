import cirq
from qramcircuits import bucket_brigade as bb
from qramcircuits.toffoli_decomposition import ToffoliDecompType
from utils import counting_utils as cu
import math
import numpy as np


def remove_T_gates(circuit, percentage):

        if percentage >= 1.0:
            raise ValueError('Percentage needs to be lower then 100%.')
        moments_list = list(circuit)

        # find how many T gates there are and what are their position
        T_count, T_positions = cu.count_ops(circuit, [cirq.T, cirq.T ** -1], return_indices=True)

        gate_count = cu.count_num_gates(circuit)
        remove_count = int(math.ceil(T_count * percentage))

        # randomly pick indices to remove
        random_indices_to_remove = np.random.choice(T_positions, size=remove_count, replace=False)
        print(f"random indices to remove: {random_indices_to_remove}")

        # create new_moments to store gates
        new_moments = []
        position = 0
        for moment in moments_list:
            moment_ops = []
            for operation in moment:
                position += 1

                if position not in random_indices_to_remove:
                    moment_ops.append(operation)

            new_moments.append(cirq.Moment(moment_ops))

            circuit = cirq.Circuit(new_moments)
        return circuit



def main():

    n = 3
    address_qubits = [cirq.NamedQubit(f'adr_{i}') for i in range(n)]

    decomp_scenario = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4_COMPUTE,  # fan_in_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4,  # mem_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_0_UNCOMPUTE,  # fan_out_decomp
        ],
        True
    )

    bb_circuit = bb.BucketBrigade(address_qubits, decomp_scenario).construct_circuit(address_qubits)

    # print(bb_circuit)

    T_count, T_positions = cu.count_ops(bb_circuit, [cirq.T, cirq.T ** -1], return_indices=True)
    print(T_count)

    for T_positions in range(100):

        modified_bb_circuit = remove_T_gates(bb_circuit, 0.90)
        # print(modified_bb_circuit)

        # Simulate the circuit
        simulator = cirq.Simulator()
        results = simulator.run(modified_bb_circuit, repetitions=1000)
        print(results.histogram(key='r'))


if __name__ == "__main__":
    main()
