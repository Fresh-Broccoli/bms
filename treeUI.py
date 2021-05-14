import tkinter as tk
import tkinter.ttk as ttk
import re

from file_messer import *

# Taken from: https://www.askpython.com/python-modules/tkinter/tkinter-treeview-widget
# Modified by Jay Zhong to work with the bioreactor monitoring system.

class StakeholderManager(tk.Frame):
    def __init__(self, root, colnames):
        tk.Frame.__init__(self, root)
        self.received_data = None
        self.id = 0
        self.iid = 0
        self.root = root
        self.initialize_user_interface(colnames)

    def initialize_user_interface(self, colnames):
        # Configure the root object for the Application
        # self.root.title("Stakeholder Manager")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # self.root.config(background="green")

        # Set the treeview
        self.tree = ttk.Treeview(self.root, columns=colnames)

        # Set the heading (Attribute Names)
        self.tree.heading('#0', text="ID")
        for no, name in enumerate(colnames, 1):
            self.tree.heading(f'#{no}', text=name)
            self.tree.column(f'#{no}', stretch=tk.YES, anchor="center")
        self.tree.column('#0', stretch=tk.NO, width=75, anchor="center")
        self.tree.column('#1', stretch=tk.NO, width=350)

        # Might want to change the following line if you want to use this code for a different purpose.
        self.tree.grid(row=0, columnspan=1, sticky='nsew')
        self.treeview = self.tree

    def insert_data(self):
        name = tk.simpledialog.askstring(title="Add Stakeholder",
                                         prompt="Name:")
        if name:
            email = tk.simpledialog.askstring(title="Add Stakeholder",
                                              prompt="Email:")
            if validate_email(email):
                with open("stakeholders.csv", "a") as stakeholders:
                    stakeholders.write(f"{name},{email}\n")
                self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                     values=(name, email))
                self.iid = self.iid + 1
                self.id = self.id + 1
            else:
                tk.messagebox.showinfo(title="Invalid Email", message="Please insert a proper email!")
        else:
            tk.messagebox.showinfo(title="Invalid Name", message="Please insert your name!")

    def insert_data_from_csv(self):
        cleanse("stakeholders.csv")
        stakeholders = open("stakeholders.csv", "r")
        stakeholders.readline()  # Skip header
        for stakeholder in stakeholders:
            name, email = stakeholder.split(",")
            self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                 values=(name, email))
            self.iid = self.iid + 1
            self.id = self.id + 1
        stakeholders.close()

    def delete_data(self, selection=None):
        try:
            if not selection:
                selected_item = self.tree.selection()[0] # get selected item
            else:
                selected_item = selection
            delete_line("stakeholders.csv", int(selected_item)+1)
            """
            with open("stakeholders.csv") as stakeholders:
                stakeholders.
            """
            self.tree.delete(selected_item)
        except IndexError:
            tk.messagebox.showinfo(title="No target", message="Can't delete, no row selected.")

    def clear_data(self):
        with open("stakeholders.csv", "w+") as f:
            f.write("Name,Email\n")
        for child in self.tree.get_children():
            self.tree.delete(child)

def validate_email(email):
    # Regex pattern taken from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    return re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email)


if __name__ == "__main__":
    app = StakeholderManager(tk.Tk(), ["Name", "Email"])
    app.root.mainloop()
