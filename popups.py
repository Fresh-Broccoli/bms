import tkinter as tk

def confirm_box(func, message, *args):
    """ Creates a confirmation box, asking the user to confirm their last action.
    Used for something important to prevent the user from accidentally doing something bad to the system.
    :param func: the function that the user wants to/accidentally run.
    :param message: The warning message that'll be displayed to the user.
    :param args: arguments supplied to func in arg form.
    """
    choice = tk.messagebox.askyesno("Confirmation", message=message)
    if choice:
        func(*args)
