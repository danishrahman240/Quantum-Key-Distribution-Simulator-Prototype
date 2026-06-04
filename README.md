# NQM Quantum Communication Prototype
This project is a Python-based simulation of quantum secure communication.
It demonstrates the BB84 Quantum Key Distribution protocol.
The system shows how Alice and Bob generate a shared secret key.
It also simulates Eve, an eavesdropper, to show how attacks increase QBER.
This project is aligned with NQM by demonstrating quantum communication concepts.
The project has three main modules: `bb84.py`, `eve.py`, and `dashboard.py`.
`bb84.py` implements key generation, basis selection, encoding, measurement, and sifting.
`eve.py` simulates eavesdropping and calculates the Quantum Bit Error Rate.
`dashboard.py` provides a visual simulator with QBER graph, network topology, and key statistics.
Run the project using: `python dashboard.py`

## Progress
- Week 1 ✓ — BB84 engine, Eve detection, live dashboard
- Week 2 Days 8–10 ✓ — Partial Eve model, key distillation, 3-node network
- Week 2 Days 11–12 ✓ — Channel noise model, upgraded dashboard
- Week 2 Days 13–14 ✓ — QKD message encryption, full pipeline test passing

## Files
| File | Purpose |
|---|---|
| bb84.py | Core BB84 quantum key exchange protocol |
| eve.py | Eve eavesdropping attack + QBER calculator |
| privacy.py | Error correction + privacy amplification |
| network.py | 3-node trusted relay quantum network |
| noise.py | Photon loss + bit-flip channel noise model |
| dashboard.py | Live interactive simulation dashboard |

## How to Run
pip install matplotlib numpy
python dashboard.py
