import random
"""import matplotlib.pyplot as plt"""

from bb84 import (
    generate_bits,
    generate_bases,
    encode_qubits,
    measure_qubits,
    sift_key
)


def eve_intercept(qubits, alice_bases):
    """
    This function simulates Eve, the hacker/eavesdropper.

    Eve intercepts Alice's qubits before they reach Bob.
    Eve randomly chooses bases to measure the qubits.
    If Eve chooses the wrong basis, she disturbs the qubit.
    """

    eve_bases = generate_bases(len(qubits))

    # This list will store the qubits after Eve touches them
    disturbed = []


    for q, ab, eb in zip(qubits, alice_bases, eve_bases):

        # If Alice's basis and Eve's basis are same,
        # Eve measures correctly, so no disturbance happens
        if ab == eb:
            disturbed.append(q)

        # If Eve uses the wrong basis,
        # the qubit gets disturbed
        else:
            disturbed.append(random.choice(['|0>', '|1>', '|+>', '|->']))

    # Return the qubits after Eve's interception
    return disturbed


def compute_qber(alice_key, bob_key, sample=50):
    """
    QBER = Quantum Bit Error Rate

    This function compares Alice's key and Bob's key.
    It checks how many bits are different.
    More difference means more error.
    More error may mean Eve is present.
    """

    # Choose how many key bits to check
    # But if key length is less than 50, check only available bits
    check = min(sample, len(alice_key))

    # Count how many bits are different between Alice and Bob
    errors = sum(
        a != b
        for a, b in zip(alice_key[:check], bob_key[:check])
    )

    # Calculate error percentage
    # Formula: QBER = errors / checked bits × 100
    if check > 0:
        return round(errors / check * 100, 1)
    else:
        return 0


def run_with_eve(n=300, eve_present=True):
    """
    This is the main function.

    It runs BB84 key generation.
    It can run in two ways:

    1. Without Eve
    2. With Eve
    """

    # Alice creates random secret bits
    alice_bits = generate_bits(n)

    # Alice chooses random bases for encoding
    alice_bases = generate_bases(n)

    # Bob chooses random bases for measuring
    bob_bases = generate_bases(n)

    # Alice converts her bits into qubit states
    qubits = encode_qubits(alice_bits, alice_bases)

    # If Eve is present, she intercepts the qubits
    if eve_present:
        qubits = eve_intercept(qubits, alice_bases)

    # Bob measures the qubits using his random bases
    bob_bits = measure_qubits(qubits, alice_bases, bob_bases)

    # Alice and Bob keep only the bits where their bases match
    alice_key, bob_key = sift_key(
        alice_bits,
        bob_bits,
        alice_bases,
        bob_bases
    )

    # Calculate error percentage between Alice's and Bob's keys
    qber = compute_qber(alice_key, bob_key)

    # If QBER is greater than 11%, assume Eve is detected
    if qber > 11:
        status = "\033[94mSECURITY ALERT: Eavesdropper detected!\033[0m"
    else:
        status = "\033[92mSecure — no eavesdropper\033[0m"

    # Print final result
    print(f"\nEve present : {eve_present}")
    print(f"QBER        : {qber}%")
    print(f"Status      : {status}")

    # Return values for further use
    return qber, status

def run_experiment_20_times():
    # Lists to store QBER values
    qber_no_eve = []
    qber_eve = []

    # Run BB84 10 times without Eve
    for i in range(10):
        qber, status = run_with_eve(n=300, eve_present=False)
        qber_no_eve.append(qber)

    # Run BB84 10 times with Eve
    for i in range(10):
        qber, status = run_with_eve(n=300, eve_present=True)
        qber_eve.append(qber)

    # Print stored QBER values
    print("\nQBER values without Eve:")
    print(qber_no_eve)

    print("\nQBER values with Eve:")
    print(qber_eve)

    return qber_no_eve, qber_eve


"""def plot_qber(qber_no_eve, qber_eve):
    # Create x-axis values: run numbers 1 to 10
    runs = range(1, 11)

    # Plot QBER without Eve using blue line
    plt.plot(runs, qber_no_eve, color="blue", marker="o", label="No Eve")

    # Plot QBER with Eve using red line
    plt.plot(runs, qber_eve, color="red", marker="o", label="Eve Present")

    # Draw dashed horizontal threshold line at 11%
    plt.axhline(y=11, color="black", linestyle="--", label="QBER Threshold = 11%")

    # Add graph title and labels
    plt.title("QBER Comparison: With Eve vs Without Eve")
    plt.xlabel("Experiment Run")
    plt.ylabel("QBER (%)")

    # Show run numbers clearly
    plt.xticks(runs)

    # Show legend
    plt.legend()

    # Show grid for easy reading
    plt.grid(True)

    # Display the graph
    plt.show()
    plt.savefig('qber_comparison.png', dpi=150)
    
    this code is to view the QBER comparison graph after running the experiments 20 times. It plots two lines: one for QBER without Eve and one for QBER with Eve, along with a threshold line at 11%. The graph includes titles, labels, legends, and grid for better visualization."""

# Program starts from here
if __name__ == "__main__":

    # First run: Eve is not present
    run_with_eve(eve_present=False)

    # Second run: Eve is present
    run_with_eve(eve_present=True)

"""if __name__ == "__main__":
    qber_no_eve, qber_eve = run_experiment_20_times()

    plot_qber(qber_no_eve, qber_eve)
    
    This code runs the experiment 20 times (10 times without Eve and 10 times with Eve) and then plots the QBER comparison graph. The graph will show how the presence of Eve affects the QBER, with a clear threshold line to indicate when Eve is likely detected."""
