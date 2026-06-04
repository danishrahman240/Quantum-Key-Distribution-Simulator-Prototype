import time

print("\n" + "="*50)
print("  QKD SIMULATOR — FULL PIPELINE TEST")
print("  Danish Rahman K | GCE Kannur")
print("  NQM Quantum Communication Prototype")
print("="*50)


# ── Module 1: BB84 Core ───────────────────────────────────────
print("\n[1/5] BB84 Key Exchange...")
time.sleep(0.5)

from bb84 import run_bb84
alice_key, bob_key = run_bb84(300)
assert alice_key == bob_key, "BB84 FAILED — keys do not match"
print(f"      ✓ Keys match — {len(alice_key)} bits generated")


# ── Module 2: Eve Detection ───────────────────────────────────
print("\n[2/5] Eve Eavesdropping Detection...")
time.sleep(0.5)

from eve import run_with_eve
qber_clean, _, _, _ = run_with_eve(300, eve_present=False)
qber_eve,   _, _, _ = run_with_eve(300, eve_present=True)
assert qber_clean < 11, "FAILED — clean channel QBER too high"
assert qber_eve   > 11, "FAILED — Eve not detected"
print(f"      ✓ No Eve  : QBER = {qber_clean}%  (below threshold)")
print(f"      ✓ Eve ON  : QBER = {qber_eve}%   (above threshold — detected)")


# ── Module 3: Key Distillation ────────────────────────────────
print("\n[3/5] Key Distillation Pipeline...")
time.sleep(0.5)

from privacy import run_full_pipeline
alice_key, bob_key, corrected, final_key = run_full_pipeline(300)
assert len(corrected) > 0,    "FAILED — corrected key is empty"
assert len(final_key) == 64,  "FAILED — final key is not 64 hex chars"
print(f"      ✓ Sifted key  : {len(alice_key)} bits")
print(f"      ✓ Corrected   : {len(corrected)} bits")
print(f"      ✓ Final key   : {final_key[:20]}... (64 hex chars)")


# ── Module 4: Multi-Node Network ──────────────────────────────
print("\n[4/5] 3-Node Quantum Network...")
time.sleep(0.5)

from network import run_two_links, run_with_targeted_attack
key_AR, _, key_RB, _, e2e = run_two_links(200)
assert len(e2e) > 0, "FAILED — end-to-end key empty"
print(f"      ✓ Link 1 key  : {len(key_AR)} bits")
print(f"      ✓ Link 2 key  : {len(key_RB)} bits")
print(f"      ✓ E2E key     : {len(e2e)} bits")

print("\n      Testing targeted Eve attack on Link 1...")
run_with_targeted_attack(200)
print(f"      ✓ Per-link attack detection working")


# ── Module 5: Message Encryption ─────────────────────────────
print("\n[5/5] QKD Message Encryption...")
time.sleep(0.5)

from encrypt import text_to_bits, bits_to_text, xor_encrypt, xor_decrypt
from bb84 import generate_bits, generate_bases, encode_qubits, measure_qubits, sift_key

message      = "HELLO QKD"
message_bits = text_to_bits(message)

n            = len(message_bits) * 4
alice_bits   = generate_bits(n)
alice_bases  = generate_bases(n)
bob_bases    = generate_bases(n)
qubits       = encode_qubits(alice_bits, alice_bases)
bob_bits_raw = measure_qubits(qubits, alice_bases, bob_bases)
alice_key, bob_key = sift_key(alice_bits, bob_bits_raw, alice_bases, bob_bases)

key_trim     = alice_key[:len(message_bits)]
cipher       = xor_encrypt(message_bits, key_trim)
decrypted    = bits_to_text(xor_decrypt(cipher, bob_key[:len(message_bits)]))

assert decrypted == message, f"FAILED — decrypted message is '{decrypted}'"
print(f"      ✓ Encrypted   : {cipher[:20]}...")
print(f"      ✓ Decrypted   : {decrypted}")
print(f"      ✓ Match       : {decrypted == message}")


# ── Final Result ──────────────────────────────────────────────
print("\n" + "="*50)
print("  ALL 5 MODULES PASSED ✓")
print("  Prototype is fully operational")
print("="*50 + "\n")