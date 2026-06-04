import random
import matplotlib.pyplot as plt

from bb84 import (
    generate_bits,
    generate_bases,
    encode_qubits,
    measure_qubits,
    sift_key
)


def eve_intercept(qubits, alice_bases, intercept_rate=1.0):
    """
    Simulates Eve the eavesdropper.
    intercept_rate: fraction of qubits Eve attacks (0.0 to 1.0)
    - 1.0 = Eve attacks all qubits
    - 0.5 = Eve attacks half the qubits
    - 0.0 = Eve attacks nothing (no disturbance)
    """
    eve_bases = generate_bases(len(qubits))
    disturbed = []

    for q, ab, eb in zip(qubits, alice_bases, eve_bases):
        if random.random() < intercept_rate:
            # Same basis → Eve gets correct state, no disturbance
            if ab == eb:
                disturbed.append(q)
            # Different basis → qubit is randomly disturbed
            else:
                disturbed.append(random.choice(['|0>', '|1>', '|+>', '|->']))
        else:
            # Eve leaves this qubit untouched
            disturbed.append(q)

    return disturbed


def compute_qber(alice_key, bob_key, sample=50):
    """
    Quantum Bit Error Rate — fraction of mismatched bits between Alice and Bob.
    Higher QBER means more disturbance, likely caused by Eve.
    Threshold: QBER > 11% → Eve is detected.
    """
    check = min(sample, len(alice_key))
    errors = sum(a != b for a, b in zip(alice_key[:check], bob_key[:check]))
    return round(errors / check * 100, 1) if check > 0 else 0


def run_with_eve(n=300, eve_present=True, intercept_rate=1.0, noise_rate=0.0):
    """
    Runs the full BB84 protocol with optional Eve.
    Returns: (qber, status_string)
    """
    alice_bits  = generate_bits(n)
    alice_bases = generate_bases(n)
    bob_bases   = generate_bases(n)
    qubits      = encode_qubits(alice_bits, alice_bases)

    if eve_present:
        qubits = eve_intercept(qubits, alice_bases, intercept_rate)

    bob_bits            = measure_qubits(qubits, alice_bases, bob_bases)
    # Apply channel noise if specified
    if noise_rate > 0:
        from noise import apply_noise
        bob_bits = apply_noise(bob_bits, noise_rate)

    alice_key, bob_key  = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    qber                = compute_qber(alice_key, bob_key)

    if qber > 11:
        status = "\033[91mSECURITY ALERT: Eavesdropper detected!\033[0m"
    else:
        status = "\033[92mSecure — no eavesdropper\033[0m"

    print(f"Eve present : {eve_present}  |  Intercept rate : {intercept_rate}  |  QBER : {qber}%  |  {status}")
    return qber, status, alice_key, bob_key


def run_eve_30_times():
    """
    Day 8 — Task 1:
    Run BB84 with Eve ON (100% intercept) 30 times.
    Logs all QBER values and prints the average.
    """
    print("\n--- Task 1: Eve ON (100% intercept) — 30 runs ---")
    results = [run_with_eve(300, True, intercept_rate=1.0)[0] for _ in range(30)]
    average_qber = sum(results) / len(results)
    print(f"\nAll QBER values : {results}")
    print(f"Average QBER    : {average_qber:.1f}%")
    return results, average_qber


def plot_qber_vs_intercept_rate():
    """
    Day 8 — Task 3:
    Plots QBER vs Eve's intercept rate (0% to 100%).
    Saves graph as eve_rate_graph.png.
    """
    print("\n--- Task 3: QBER vs Eve intercept rate ---")
    intercept_rates = [i / 10 for i in range(11)]   # 0.0, 0.1, ... 1.0
    avg_qbers = []

    for rate in intercept_rates:
        results  = [run_with_eve(300, True, intercept_rate=rate)[0] for _ in range(20)]
        avg_qber = sum(results) / len(results)
        avg_qbers.append(avg_qber)
        print(f"Intercept rate = {int(rate*100):3d}%  →  Avg QBER = {avg_qber:.1f}%")

    x_labels = [int(r * 100) for r in intercept_rates]

    plt.figure(figsize=(9, 5))
    plt.plot(x_labels, avg_qbers, color='#E24B4A', marker='o', linewidth=2, markersize=6)
    plt.axhline(y=11, color='black', linestyle='--', linewidth=1.5, label='Detection threshold (11%)')
    plt.fill_between(x_labels, 11, avg_qbers,
                     where=[q > 11 for q in avg_qbers],
                     alpha=0.15, color='#E24B4A', label='Eve detectable zone')
    plt.title("QBER vs Eve Intercept Rate", fontsize=13, fontweight='bold')
    plt.xlabel("Eve Intercept Rate (%)")
    plt.ylabel("Measured QBER (%)")
    plt.xticks(x_labels)
    plt.ylim(0, 32)
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("eve_rate_graph.png", dpi=150)
    print("\nGraph saved → eve_rate_graph.png")
    plt.show()

    return x_labels, avg_qbers


if __name__ == "__main__":
    # Task 1 — 30 runs with full Eve, print average QBER
    run_eve_30_times()

    # Task 3 — Plot QBER vs Eve intercept rate and save graph
    plot_qber_vs_intercept_rate()