import random
from bb84 import generate_bits, generate_bases, encode_qubits, measure_qubits, sift_key


def text_to_bits(text):
    bits = []
    for char in text:
        char_bits = format(ord(char), '08b')
        bits.extend([int(b) for b in char_bits])
    return bits


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        ascii_val = int(''.join(map(str, byte)), 2)
        chars.append(chr(ascii_val))
    return ''.join(chars)


def xor_encrypt(message_bits, key_bits):
    if len(key_bits) < len(message_bits):
        print("ERROR: Key shorter than message.")
        return None
    return [m ^ k for m, k in zip(message_bits, key_bits)]


def xor_decrypt(cipher_bits, key_bits):
    return [c ^ k for c, k in zip(cipher_bits, key_bits)]


def corrupt_key(key_bits, error_rate=0.5):
    return [
        random.randint(0, 1) if random.random() < error_rate else bit
        for bit in key_bits
    ]


def run_encryption_demo():
    message      = "HELLO QKD"
    message_bits = text_to_bits(message)

    print(f"\n{'='*42}")
    print(f"  QKD Message Encryption Demo")
    print(f"{'='*42}")
    print(f"  Original message : {message}")
    print(f"  Message length   : {len(message_bits)} bits needed")

    # Generate shared key via BB84
    n            = len(message_bits) * 4
    alice_bits   = generate_bits(n)
    alice_bases  = generate_bases(n)
    bob_bases    = generate_bases(n)
    qubits       = encode_qubits(alice_bits, alice_bases)
    bob_bits_raw = measure_qubits(qubits, alice_bases, bob_bases)
    alice_key, bob_key = sift_key(alice_bits, bob_bits_raw, alice_bases, bob_bases)

    print(f"  Qubits sent      : {n}")
    print(f"  Sifted key length: {len(alice_key)} bits")

    if len(alice_key) < len(message_bits):
        print("  Key too short — re-run.")
        return

    alice_key_trimmed = alice_key[:len(message_bits)]
    bob_key_trimmed   = bob_key[:len(message_bits)]

    # Alice encrypts
    cipher_bits = xor_encrypt(message_bits, alice_key_trimmed)
    print(f"\n  [Alice] Ciphertext (first 40 bits):")
    print(f"  {cipher_bits[:40]}...")

    # Bob decrypts
    bob_decrypted_bits = xor_decrypt(cipher_bits, bob_key_trimmed)
    bob_message        = bits_to_text(bob_decrypted_bits)
    print(f"\n  [Bob]   Decrypted message    : {bob_message}")
    if bob_message == message:
        print("  [Bob]   Status               : \033[92m✓ Message received correctly\033[0m")
    else:
        print("  [Bob]   Status               : \033[91m✗ Decryption failed\033[0m")

    # Eve tries with corrupted key
    eve_key            = corrupt_key(alice_key_trimmed, error_rate=0.5)
    eve_decrypted_bits = xor_decrypt(cipher_bits, eve_key)
    eve_message        = bits_to_text(eve_decrypted_bits)
    print(f"\n  [Eve]   Decrypted message    : {eve_message}")
    print(f"  [Eve]   Status               : \033[91m✗ Garbage — decryption failed\033[0m")
    print(f"\n{'='*42}")


if __name__ == "__main__":
    run_encryption_demo()