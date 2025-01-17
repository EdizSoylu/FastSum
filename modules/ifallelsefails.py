import tkinter as tk
from tkinter import messagebox


def imhopeless(parent):

    def celsius_to_fahrenheit():
        try:
            celsius = float(entry.get())
            fahrenheit = (celsius * 9/5) + 32
            result_label.config(text=f"{celsius:.2f}°C = {fahrenheit:.2f}°F")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def fahrenheit_to_celsius():
        try:
            fahrenheit = float(entry.get())
            celsius = (fahrenheit - 32) * 5/9
            result_label.config(text=f"{fahrenheit:.2f}°F = {celsius:.2f}°C")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    root = tk.Toplevel(parent)
    root.title("Temperature Converter")
    root.geometry("300x200")
    root.resizable(False, False)

    entry_label = tk.Label(root, text="Enter Temperature:", font=("Arial", 12))
    entry_label.pack(pady=5)
    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    c_to_f_button = tk.Button(button_frame, text="C to F", command=celsius_to_fahrenheit, width=10)
    c_to_f_button.pack(side="left", padx=5)

    f_to_c_button = tk.Button(button_frame, text="F to C", command=fahrenheit_to_celsius, width=10)
    f_to_c_button.pack(side="right", padx=5)

    result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
    result_label.pack(pady=10)

    root.mainloop()
