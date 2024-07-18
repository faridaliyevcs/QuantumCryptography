import tkinter as tk
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.visualization import plot_histogram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


def create_ghz_state(qc, qubits):
    qc.h(qubits[0])
    qc.cx(qubits[0], qubits[1])
    qc.cx(qubits[1], qubits[2])


def measure_in_basis(qc, qubit, cbit, basis):
    if basis == 'X':
        qc.h(qubit)
    elif basis == 'Y':
        qc.sdg(qubit)
        qc.h(qubit)
    qc.measure(qubit, cbit)


def qss_protocol():
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)

    create_ghz_state(qc, qr)

    bases = ['X', 'Y', 'Z']
    alice_basis = random.choice(bases)
    bob_basis = random.choice(bases)
    charlie_basis = random.choice(bases)

    measure_in_basis(qc, qr[0], cr[0], alice_basis)
    measure_in_basis(qc, qr[1], cr[1], bob_basis)
    measure_in_basis(qc, qr[2], cr[2], charlie_basis)

    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1)
    result = job.result()
    counts = result.get_counts(qc)

    return counts, alice_basis, bob_basis, charlie_basis


def run_qss_protocol():
    counts, alice_basis, bob_basis, charlie_basis = qss_protocol()
    result_text.set(f"Measurement Results: {counts}\n"
                    f"Basis chosen: Alice - {alice_basis}, Bob - {bob_basis}, Charlie - {charlie_basis}")

    fig = plot_histogram(counts)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


window = tk.Tk()
window.title("Quantum Secret Sharing Protocol")

frame = tk.Frame(window)
frame.pack(pady=20)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify='left')
result_label.pack()

run_button = tk.Button(window, text="Run QSS Protocol", command=run_qss_protocol)
run_button.pack(pady=10)

window.mainloop()
