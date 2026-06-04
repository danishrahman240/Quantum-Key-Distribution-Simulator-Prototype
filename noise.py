import random
import matplotlib.pyplot as plt
from bb84 import generate_bits, generate_bases, encode_qubits, measure_qubits, sift_key


def apply_loss(qubits, alice_bases, alice_bits, loss_rate=0.1):
    """
    Simulates photon loss in the quantum channel.
    Returns only surviving qubits with their matching bases and bits.
    """
    survived_qubits = []
    survived_bases  = []
    survived_bits   = []

    for q, base, bit in zip(qubits, alice_bases, alice_bits):
        if random.random() > loss_rate:
            survived_qubits.append(q)
            survived_bases.append(base)
            survived_bits.append(bit)

    return survived_qubits, survived_bases, survived_bits


def apply_noise(bob_bits, noise_rate=0.02):
    """
    Simulates bit-flip noise in Bob's measurements.
    2% noise rate is realistic for short-distance fiber QKD.
    """
    return [bit ^ 1 if random.random() < noise_rate else bit for bit in bob_bits]


def plot_key_rate_vs_loss():
    """
    Plots average sifted key length vs channel loss rate.
    Saves graph as key_rate_vs_loss.png
    """
    loss_rates      = [i / 10 for i in range(9)]   # 0.0 to 0.8
    avg_key_lengths = []

    print("\n--- Key Rate vs Channel Loss ---")

    for loss in loss_rates:
        key_lengths = []

        for _ in range(20):
            n              = 300
            alice_bits     = generate_bits(n)
            alice_bases    = generate_bases(n)
            qubits         = encode_qubits(alice_bits, alice_bases)

            survived_qubits, survived_alice_bases, survived_alice_bits = apply_loss(
                qubits, alice_bases, alice_bits, loss_rate=loss
            )

            survived_bob_bases = generate_bases(len(survived_qubits))
            bob_bits           = measure_qubits(survived_qubits, survived_alice_bases, survived_bob_bases)
            bob_bits           = apply_noise(bob_bits, noise_rate=0.02)

            alice_key, bob_key = sift_key(survived_alice_bits, bob_bits, survived_alice_bases, survived_bob_bases)
            key_lengths.append(len(alice_key))

        avg = sum(key_lengths) / len(key_lengths)
        avg_key_lengths.append(avg)
        print(f"Loss rate = {int(loss*100):2d}%  →  Avg key length = {avg:.1f} bits")

    x_labels = [int(r * 100) for r in loss_rates]
    plt.figure(figsize=(9, 5))
    plt.plot(x_labels, avg_key_lengths, color='#185FA5', marker='o', linewidth=2, markersize=6)
    plt.fill_between(x_labels, avg_key_lengths, alpha=0.1, color='#185FA5')
    plt.title("Key Rate vs Channel Loss", fontsize=13, fontweight='bold')
    plt.xlabel("Channel Loss Rate (%)")
    plt.ylabel("Average Sifted Key Length (bits)")
    plt.xticks(x_labels)
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("key_rate_vs_loss.png", dpi=150)
    print("\nGraph saved → key_rate_vs_loss.png")
    plt.show()


if __name__ == "__main__":
    plot_key_rate_vs_loss()