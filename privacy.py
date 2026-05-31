import hashlib
from bb84 import generate_bits, generate_bases, encode_qubits, measure_qubits, sift_key


def error_correction(alice_key, bob_key):
    """
    Task 1 — Error Correction
    Keep only the bits where Alice and Bob agree.
    Discard positions where they differ.
    """
    corrected = [a for a, b in zip(alice_key, bob_key) if a == b]
    return corrected


def privacy_amplification(corrected_key):
    """
    Task 2 — Privacy Amplification
    Hash the corrected key using SHA-256.
    This removes any partial info Eve may have gained.
    """
    key_str   = ''.join(map(str, corrected_key))
    final_key = hashlib.sha256(key_str.encode()).hexdigest()
    return final_key


def run_full_pipeline(n=300):
    """
    Task 3 — Print the full pipeline from raw bits to final key.
    """
    # Step 1 — Generate raw bits and bases
    alice_bits  = generate_bits(n)
    alice_bases = generate_bases(n)
    bob_bases   = generate_bases(n)

    # Step 2 — Encode and measure
    qubits   = encode_qubits(alice_bits, alice_bases)
    bob_bits = measure_qubits(qubits, alice_bases, bob_bases)

    # Step 3 — Sift key (basis matching)
    alice_key, bob_key = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)

    # Step 4 — Error correction   ← YOUR LINE LIVES HERE INSIDE THIS FUNCTION
    corrected = error_correction(alice_key, bob_key)

    # Step 5 — Privacy amplification
    final_key = privacy_amplification(corrected)

    # Step 6 — Print full pipeline
    print(f"\n--- Full QKD Key Distillation Pipeline ---")
    print(f"Raw bits sent      : {n}")
    print(f"Sifted key length  : {len(alice_key)} bits")
    print(f"Corrected key      : {len(corrected)} bits")
    print(f"Final secure key   : {final_key}")

    return alice_key, bob_key, corrected, final_key


if __name__ == "__main__":
    run_full_pipeline()