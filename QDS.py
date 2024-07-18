import tkinter as tk
from tkinter import messagebox
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile, execute
from qiskit.visualization import plot_histogram


def create_key_pair():
    private_key = np.random.randint(2)
    if private_key == 0:
        public_key = np.array([1, 0])
    else:
        public_key = np.array([0, 1])
    return private_key, public_key


def create_signature(message, private_keys):
    circuits = []
    for i, bit in enumerate(message):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)

        if private_keys[i] == 1:
            circuit.x(qr[0])

        circuits.append(circuit)
    return circuits


def validate_signature(message, private_keys, public_keys):
    results = []
    for i, bit in enumerate(message):
        qr = QuantumRegister(3)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        if public_keys[i][1] == 1:
            circuit.x(qr[1])

        if private_keys[i] == 1:
            circuit.x(qr[2])

        circuit.cswap(qr[0], qr[1], qr[2])
        circuit.h(qr[0])
        circuit.measure(qr[0], cr[0])
        results.append(circuit)
    return results


def execute_validation_circuits(validation_circuits):
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuits = [transpile(circuit, simulator) for circuit in validation_circuits]
    results = [execute(circuit, simulator, shots=1024).result().get_counts() for circuit in compiled_circuits]
    return results


class QDSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Digital Signature (QDS)")

        self.message_label = tk.Label(root, text="Enter Message (0s and 1s):")
        self.message_label.pack()

        self.message_entry = tk.Entry(root)
        self.message_entry.pack()

        self.generate_keys_button = tk.Button(root, text="Generate Keys", command=self.generate_keys)
        self.generate_keys_button.pack()

        self.sign_message_button = tk.Button(root, text="Sign Message", command=self.sign_message)
        self.sign_message_button.pack()

        self.validate_signature_button = tk.Button(root, text="Validate Signature", command=self.validate_signature)
        self.validate_signature_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.private_keys = []
        self.public_keys = []
        self.signature_circuits = []
        self.message = []

    def generate_keys(self):
        self.message = list(map(int, self.message_entry.get()))
        self.private_keys = []
        self.public_keys = []
        for _ in self.message:
            pk, pubk = create_key_pair()
            self.private_keys.append(pk)
            self.public_keys.append(pubk)
        messagebox.showinfo("Keys Generated", "Private and Public Keys have been generated.")

    def sign_message(self):
        if not self.private_keys:
            messagebox.showerror("Error", "Please generate keys first.")
            return
        self.signature_circuits = create_signature(self.message, self.private_keys)
        messagebox.showinfo("Message Signed", "The message has been signed.")

    def validate_signature(self):
        if not self.signature_circuits:
            messagebox.showerror("Error", "Please sign the message first.")
            return
        validation_circuits = validate_signature(self.message, self.private_keys, self.public_keys)
        results = execute_validation_circuits(validation_circuits)
        for i, result in enumerate(results):
            validation_result = result.get('0', 0) / 1024
            if validation_result > 0.5:
                self.result_label.config(text=f"Bit {i} validation: Pass")
            else:
                self.result_label.config(text=f"Bit {i} validation: Fail")
        plot_histogram(results[0])


root = tk.Tk()
app = QDSApp(root)
root.mainloop()
