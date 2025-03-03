import subprocess
import time
from pathlib import Path

import numpy as np

Path("./results").mkdir(parents=True, exist_ok=True)


def get_stream_length(file_path):
    """
    Get the number of bits in a binary file.

    :param file_path: Path to the binary file.
    :return: Number of bits in the file.
    """
    with open(file_path, "rb") as f:
        byte_data = f.read()
    bit_count = len(byte_data) * 8  # Convert bytes to bits
    print(f"Stream length: {bit_count} bits")
    return bit_count


def run_nist_test(binary_file_path):
    nist_tool = "./../../nist/assess"  # Ensure NIST tool path is correct
    bit_length = get_stream_length(binary_file_path)
    try:
        result = subprocess.run(
            [nist_tool, str(bit_length), binary_file_path],
            stdout=subprocess.PIPE,
            text=True,
        )
        print("NIST Test Results:")
        print(result.stdout)
    except Exception as e:
        print("Error running NIST test:", e)


def gauss_map_prng(alpha=4.9, beta=0.5, size=1000):
    """
    Generate a sequence of pseudo-random numbers using the Gauss Map.

    :param alpha: Control parameter for steepness (alpha > 0).
    :param beta: Shift parameter (-1 < beta < 1).
    :param seed: Initial state x0.
    :param size: Number of random numbers to generate.
    :return: List of pseudo-random numbers.
    """
    sequence = []
    state = (time.time_ns() % 1_000_000) / 1_000_000
    alpha = alpha + (state * 0.001)
    print(state)
    for _ in range(size):
        state = np.exp(-alpha * state**2) + beta
        sequence.append(state % 1)  # Keep values within [0, 1]
    return sequence


def convert_to_bits(sequence):
    """
    Convert a sequence of numbers in [0, 1] to binary bits (0 or 1).

    :param sequence: List of floating-point numbers.
    :return: List of binary bits.
    """
    return [1 if num > 0.5 else 0 for num in sequence]


def save_to_binary_file(sequence, filename="./results/prng_output.bin"):
    with open(filename, "wb") as f:
        byte_arr = bytearray()
        for i in range(0, len(sequence), 8):
            byte = sum([bit << (7 - j) for j, bit in enumerate(sequence[i : i + 8])])
            byte_arr.append(byte)
        f.write(byte_arr)


# Example Usage
random_sequence = gauss_map_prng(alpha=4.9, beta=-0.5, size=1_000_000)
binary_sequence = convert_to_bits(random_sequence)

# Assuming `binary_sequence` contains your PRNG bit sequence
save_to_binary_file(binary_sequence)
print("Binary file saved as prng_output.bin")

run_nist_test("./results/prng_output.bin")
# print("First 10 Random Numbers:", random_sequence)
