from bb84 import run_bb84
from eve import compute_qber, run_with_eve


def get_status(qber):
    if qber > 11:
        return "SECURITY ALERT — Eavesdropper detected! ✗"
    else:
        return "Secure ✓"


def run_two_links(n=200):
    # --- Link 1: Alice to Relay ---
    print("Running Link 1: Alice → Relay")
    key_AR, relay_from_alice = run_bb84(n)

    # --- Link 2: Relay to Bob ---
    print("Running Link 2: Relay → Bob")
    key_RB, bob_key = run_bb84(n)

    # --- Compute QBER for each link ---
    qber_link1 = compute_qber(key_AR, relay_from_alice)
    qber_link2 = compute_qber(key_RB, bob_key)

    # --- XOR both keys for end-to-end key ---
    e2e_len        = min(len(key_AR), len(key_RB))
    end_to_end_key = [a ^ b for a, b in zip(key_AR[:e2e_len], key_RB[:e2e_len])]

    # --- Print status table ---
    print("\n" + "="*34)
    print("     QKD Network Status Table")
    print("="*34)

    print(f"\nLink 1 (Alice → Relay)")
    print(f"  Key length : {len(key_AR)} bits")
    print(f"  QBER       : {qber_link1}%")
    print(f"  Status     : {get_status(qber_link1)}")

    print(f"\nLink 2 (Relay → Bob)")
    print(f"  Key length : {len(key_RB)} bits")
    print(f"  QBER       : {qber_link2}%")
    print(f"  Status     : {get_status(qber_link2)}")

    print(f"\nEnd-to-end key length : {e2e_len} bits")
    print("="*34)

    return key_AR, relay_from_alice, key_RB, bob_key, end_to_end_key

def run_with_targeted_attack(n=200):
    """
    Task 3 — Eve attacks Link 1 only.
    Link 2 runs clean with no Eve.
    Shows per-link security monitoring.
    """

    # --- Link 1: Alice to Relay — WITH Eve attacking ---
    print("Running Link 1: Alice → Relay  [Eve is attacking this link]")
    qber_link1, _, key_AR, relay_from_alice = run_with_eve(
        n=n,
        eve_present=True,
        intercept_rate=1.0
    )

    # --- Link 2: Relay to Bob — NO Eve ---
    print("Running Link 2: Relay → Bob    [Clean — no Eve]")
    key_RB, bob_key = run_bb84(n)
    qber_link2 = compute_qber(key_RB, bob_key)

    # --- XOR both keys for end-to-end key ---
    e2e_len        = min(len(key_AR), len(key_RB))
    end_to_end_key = [a ^ b for a, b in zip(key_AR[:e2e_len], key_RB[:e2e_len])]

    # --- Print status table ---
    print("\n" + "="*34)
    print("  QKD Network — Targeted Attack")
    print("="*34)

    print(f"\nLink 1 (Alice → Relay)  ← Eve here")
    print(f"  Key length : {len(key_AR)} bits")
    print(f"  QBER       : {qber_link1}%")
    print(f"  Status     : {get_status(qber_link1)}")

    print(f"\nLink 2 (Relay → Bob)    ← Clean")
    print(f"  Key length : {len(key_RB)} bits")
    print(f"  QBER       : {qber_link2}%")
    print(f"  Status     : {get_status(qber_link2)}")

    print(f"\nEnd-to-end key length : {e2e_len} bits")

    # Network-level decision
    if qber_link1 > 11 or qber_link2 > 11:
        print("\n⚠  Network verdict : KEY EXCHANGE ABORTED")
        print("   Reason          : Compromised link detected")
    else:
        print("\n✓  Network verdict : Key exchange successful")

    print("="*34)

    return key_AR, key_RB, end_to_end_key

if __name__ == "__main__":
    print("\n========== TEST 1: No Eve ==========")
    run_two_links()

    print("\n========== TEST 2: Eve on Link 1 ==========")
    run_with_targeted_attack()