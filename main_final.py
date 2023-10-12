import cirq
from qramcircuits import bucket_brigade as bb
from qramcircuits.toffoli_decomposition import ToffoliDecompType
from utils import counting_utils as cu
import math
import numpy as np
import optimizers as qopt
import matplotlib.pyplot as plt
import itertools

# def all_possible_addresses(num_qubits):
#     return itertools.product([0, 1], repeat=num_qubits)

def remove_T_gates(circuit, percentage):

        if percentage >= 1.0:
            raise ValueError('Percentage needs to be lower then 100%.')
        moments_list = list(circuit)

        # find how many T gates there are and what are their position
        T_count, T_positions = cu.count_ops(circuit, [cirq.T, cirq.T ** -1], return_indices=True)

        # print(T_count)
        # print(T_positions)
        # gate_count = cu.count_num_gates(circuit)
        remove_count = int(math.ceil(T_count * percentage))
        # print(f"remove count{remove_count}")

        # randomly pick indices to remove
        random_indices_to_remove = np.random.choice(T_positions, size=remove_count, replace=False)
        # print(f"random indices to remove: {random_indices_to_remove}")

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

    no_decomp = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.NO_DECOMP,
            ToffoliDecompType.NO_DECOMP,
            ToffoliDecompType.NO_DECOMP
        ],
        True
    )

    bb_circuit = bb.BucketBrigade(address_qubits, decomp_scenario).construct_circuit(address_qubits)

    # Initialising Addressing qubits
    # bb_circuit.insert(0, cirq.X(address_qubits[0]))
    # bb_circuit.insert(0, cirq.X(address_qubits[1]))
    # bb_circuit.insert(0, cirq.X(address_qubits[2]))

    print(bb_circuit)

    percentages = [0.05, 0.10, 0.15]

    for percentage in percentages:
        total_count_ones = 0
        print(f"percentage{percentage}")

        for _ in range(1000):
            modified_bb_circuit = remove_T_gates(bb_circuit, percentage)
            simulator = cirq.Simulator()
            results = simulator.run(modified_bb_circuit, repetitions=1000)
            # print(results.histogram(key='r'))
            count_ones = sum(results.data['r'])

            # print(count_ones)
            if count_ones == 1000:
                total_count_ones += 1
                # print(total_count_ones)
        print(f"average count: {total_count_ones}")


if __name__ == "__main__":
    main()
