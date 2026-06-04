import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, Slider
import random
from eve import run_with_eve, compute_qber
from bb84 import generate_bits, generate_bases, encode_qubits, measure_qubits, sift_key
from noise import apply_loss, apply_noise


# ── Figure setup ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle(
    "NQM Quantum Communication Prototype\n"
    "Danish Rahman K | Government College of Engineering Kannur",
    fontsize=13,
    fontweight='bold',
    y=0.98
)
plt.subplots_adjust(bottom=0.25, top=0.88, wspace=0.4)

# ── State variables ───────────────────────────────────────────
qber_history = []
run_count    = [0]
eve_mode     = [False]
noise_rate   = [0.02]

# ── Summary text placeholder (created once) ───────────────────
summary_text_obj = fig.text(
    0.5, 0.01, '',
    ha='center', fontsize=10, fontweight='bold', color='#1D9E75',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F8F8',
              edgecolor='#1D9E75', linewidth=1.5)
)


# ── Core simulation ───────────────────────────────────────────
def run_simulation(_=None):
    run_count[0] += 1
    qber, status, _,_= run_with_eve(
        n=300,
        eve_present=eve_mode[0],
        noise_rate=noise_rate[0]
    )
    qber_history.append(qber)
    if len(qber_history) > 20:
        qber_history.pop(0)
    update_plots(qber, status)


def update_plots(qber, status):

    # ── Plot 1: QBER over time ─────────────────────────────────
    ax = axes[0]
    ax.clear()
    ax.plot(qber_history, color='#185FA5', linewidth=2, marker='o', markersize=4)
    ax.axhline(y=11, color='#E24B4A', linestyle='--', linewidth=1.5, label='Eve threshold (11%)')
    ax.set_title("QBER over runs", fontsize=11)
    ax.set_ylabel("Error rate (%)")
    ax.set_ylim(0, 45)
    ax.legend(fontsize=9)
    ax.set_facecolor('#F8F8F8')
    color = '#E24B4A' if qber > 11 else '#1D9E75'
    ax.text(0.5, 0.88, f"Current QBER: {qber}%", transform=ax.transAxes,
            ha='center', fontsize=11, fontweight='bold', color=color)

    # ── Plot 2: Network diagram ────────────────────────────────
    ax2 = axes[1]
    ax2.clear()
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 5)
    ax2.set_title("Network topology", fontsize=11)
    ax2.axis('off')
    ax2.set_facecolor('#F8F8F8')

    nodes = [
        ('Alice', 1.5, 2.5, '#185FA5'),
        ('Relay', 5.0, 2.5, '#1D9E75'),
        ('Bob',   8.5, 2.5, '#185FA5')
    ]
    for name, x, y, c in nodes:
        ax2.add_patch(plt.Circle((x, y), 0.7, color=c, zorder=3))
        ax2.text(x, y, name[0], ha='center', va='center',
                 color='white', fontweight='bold', fontsize=12, zorder=4)
        ax2.text(x, y - 1.1, name, ha='center', fontsize=9)

    link_color = '#E24B4A' if eve_mode[0] else '#1D9E75'

    # Link 1 arrow
    ax2.annotate('', xy=(4.3, 2.5), xytext=(2.2, 2.5),
                 arrowprops=dict(arrowstyle='->', color=link_color, lw=2))
    link1_qber = qber if eve_mode[0] else round(noise_rate[0] * 100 * 0.5, 1)
    ax2.text(3.25, 2.9, f"QBER: {link1_qber}%", ha='center', fontsize=8,
             color='#E24B4A' if link1_qber > 11 else '#1D9E75')

    # Link 2 arrow — always clean
    ax2.annotate('', xy=(7.8, 2.5), xytext=(5.7, 2.5),
                 arrowprops=dict(arrowstyle='->', color='#1D9E75', lw=2))
    ax2.text(6.75, 2.9, "QBER: 0.0%", ha='center', fontsize=8, color='#1D9E75')

    # Eve node
    if eve_mode[0]:
        ax2.add_patch(plt.Circle((3.25, 3.8), 0.5, color='#E24B4A', zorder=3))
        ax2.text(3.25, 3.8, 'E', ha='center', va='center',
                 color='white', fontweight='bold', fontsize=12, zorder=4)
        ax2.text(3.25, 3.1, 'Eve', ha='center', fontsize=9, color='#E24B4A')

    channel_text = "Channel: COMPROMISED" if eve_mode[0] else "Channel: SECURE"
    ax2.text(5, 0.6, channel_text, ha='center', fontsize=10, fontweight='bold',
             color='#E24B4A' if eve_mode[0] else '#1D9E75')

    # ── Plot 3: Key distillation bars ─────────────────────────
    ax3 = axes[2]
    ax3.clear()
    n          = 300
    alice_bits = generate_bits(n)
    alice_bases = generate_bases(n)
    bob_bases  = generate_bases(n)
    qubits     = encode_qubits(alice_bits, alice_bases)
    bob_bits   = measure_qubits(qubits, alice_bases, bob_bases)
    alice_key, _ = sift_key(alice_bits, bob_bits, alice_bases, bob_bases)
    sifted_len   = len(alice_key)
    final_len    = max(0, sifted_len - int(sifted_len * qber / 100) - 10)
    bars = ax3.bar(
        ['Qubits sent', 'Sifted key', 'Final key'],
        [n, sifted_len, final_len],
        color=['#B5D4F4', '#5DCAA5', '#1D9E75' if not eve_mode[0] else '#F09595']
    )
    ax3.set_title("Key distillation", fontsize=11)
    ax3.set_ylabel("Bits")
    ax3.set_facecolor('#F8F8F8')
    for bar in bars:
        h = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2, h + 3,
                 str(int(h)), ha='center', fontsize=9)

    # ── Security summary bar ───────────────────────────────────
    summary_color = '#E24B4A' if qber > 11 else '#1D9E75'
    summary_text  = (
        f"⚠  NETWORK ALERT — Link 1 compromised | QBER: {qber}% | Key exchange aborted"
        if qber > 11 else
        f"✓  NETWORK SECURE — End-to-end key generated | QBER: {qber}% | Noise: {int(noise_rate[0] * 100)}%"
    )
    summary_text_obj.set_text(summary_text)
    summary_text_obj.set_color(summary_color)
    summary_text_obj.get_bbox_patch().set_edgecolor(summary_color)

    plt.draw()


# ── Buttons and slider — created ONCE outside update_plots ────
ax_run   = plt.axes([0.35, 0.10, 0.15, 0.05])
ax_eve   = plt.axes([0.52, 0.10, 0.15, 0.05])
ax_noise = plt.axes([0.15, 0.04, 0.25, 0.03])

btn_run = Button(ax_run, 'Run exchange')
btn_eve = Button(ax_eve, 'Toggle Eve')
slider  = Slider(ax_noise, 'Channel noise', 0.0, 0.30,
                 valinit=0.02, valstep=0.01, color='#185FA5')


def toggle_eve(_):
    eve_mode[0] = not eve_mode[0]
    btn_eve.label.set_text('Eve: ON' if eve_mode[0] else 'Eve: OFF')
    btn_eve.label.set_color('#E24B4A' if eve_mode[0] else '#1D9E75')
    run_simulation()


def update_noise(val):
    noise_rate[0] = round(slider.val, 2)
    run_simulation()


btn_run.on_clicked(run_simulation)
btn_eve.on_clicked(toggle_eve)
slider.on_changed(update_noise)

# ── First run ─────────────────────────────────────────────────
run_simulation()
plt.show()