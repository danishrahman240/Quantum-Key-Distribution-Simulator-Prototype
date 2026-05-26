import random   # used to generate random 0s and 1s


def generate_bits(n):
    # Create n random bits
    # Example output: [1, 0, 1, 1, 0]
    return [random.randint(0, 1) for _ in range(n)]


def generate_bases(n):
    # Create n random bases
    # 0 means + basis
    # 1 means x basis
    return [random.randint(0, 1) for _ in range(n)]


def encode_qubits(bits, bases):
    # This table tells which qubit state to use
    # depending on bit and basis
    state_map = {
        (0, 0): '|0>',
        (1, 0): '|1>',
        (0, 1): '|+>',
        (1, 1): '|->'
    }

    # Take each bit and basis together
    # Convert them into qubit states
    return [state_map[(b, base)] for b, base in zip(bits, bases)]


def measure_qubits(qubits, alice_bases, bob_bases):
    # This list stores Bob's measurement results
    results = []

    # Take one qubit, one Alice basis, and one Bob basis at a time
    for q, ab, bb in zip(qubits, alice_bases, bob_bases):

        # If Alice and Bob used same basis
        if ab == bb:
            # Bob gets correct bit
            results.append(int(q in ['|1>', '|->']))

        else:
            # If bases are different, Bob gets random result
            results.append(random.randint(0, 1))

    return results


def sift_key(alice_bits, bob_bits, alice_bases, bob_bases):
    # Final keys after removing wrong-basis bits
    alice_key = []
    bob_key = []

    # Check every position
    for i in range(len(alice_bases)):

        # Keep only if Alice and Bob used same basis
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])

    return alice_key, bob_key


def run_bb84(n=100):
    # Alice creates random bits
    alice_bits = generate_bits(n)

    # Alice chooses random bases
    alice_bases = generate_bases(n)

    # Bob chooses random bases
    bob_bases = generate_bases(n)

    # Alice converts bits into qubits
    qubits = encode_qubits(alice_bits, alice_bases)

    # Bob measures the qubits
    bob_bits = measure_qubits(qubits, alice_bases, bob_bases)

    # Alice and Bob keep only same-basis bits
    alice_key, bob_key = sift_key(
        alice_bits,
        bob_bits,
        alice_bases,
        bob_bases
    )

    # Print result
    print(f"Qubits sent       : {n}")
    print(f"Sifted key length : {len(alice_key)}")
    print(f"Keys match        : {alice_key == bob_key}")
    print(f"Sample key Alice  : {alice_key[:20]}")
    print(f"Sample key Bob    : {bob_key[:20]}")

    return alice_key, bob_key


# Program starts here
if __name__ == "__main__":
    run_bb84(200)