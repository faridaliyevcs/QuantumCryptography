import tkinter as tk
from tkinter import messagebox
import random

def generate_random_key(length):
    return ''.join(random.choice('01') for _ in range(length))

def xor_strings(s, t):
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(s, t))

def encrypt_message():
    message = message_entry.get()
    key = key_entry.get()

    if len(message) != len(key):
        messagebox.showerror("Error", "Message and key must have the same length.")
        return

    encrypted_message = xor_strings(message, key)
    result_label.config(text=f"Encrypted Message: {encrypted_message}")

def decrypt_message():
    encrypted_message = message_entry.get()
    key = key_entry.get()

    if len(encrypted_message) != len(key):
        messagebox.showerror("Error", "Encrypted message and key must have the same length.")
        return

    decrypted_message = xor_strings(encrypted_message, key)
    result_label.config(text=f"Decrypted Message: {decrypted_message}")

root = tk.Tk()
root.title("Quantum One-Time Pad Cryptography")

tk.Label(root, text="Message:").grid(row=0, column=0, padx=10, pady=10)
message_entry = tk.Entry(root)
message_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Key:").grid(row=1, column=0, padx=10, pady=10)
key_entry = tk.Entry(root)
key_entry.grid(row=1, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.grid(row=2, column=1, padx=10, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def generate_key():
    message_length = len(message_entry.get())
    if message_length > 0:
        random_key = generate_random_key(message_length)
        key_entry.delete(0, tk.END)
        key_entry.insert(0, random_key)
    else:
        messagebox.showerror("Error", "Enter a message first to generate a key.")

generate_key_button = tk.Button(root, text="Generate Random Key", command=generate_key)
generate_key_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
