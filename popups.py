import tkinter as tk

def confirm_box(func, message, *args):
    choice = tk.messagebox.askyesno("Confirmation", message=message)
    if choice:
        func(*args)
