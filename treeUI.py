import tkinter as tk
import tkinter.ttk as ttk


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
        email = tk.simpledialog.askstring(title="Add Stakeholder",
                                          prompt="Email:")
        if len(name+email)>1:
            self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                 values=(name,email))
            self.iid = self.iid + 1
            self.id = self.id + 1


    def insert_data_from_csv(self):
        stakeholders = open("stakeholders.csv", "r")
        stakeholders.readline() # Skip header
        for stakeholder in stakeholders:
            name, email = stakeholder.split(",")
            self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                 values=(name,email))
            self.iid = self.iid + 1
            self.id = self.id + 1
        stakeholders.close()

    def delete_data(self):
        try:
            selected_item = self.tree.selection()[0] ## get selected item
            self.tree.delete(selected_item)
        except IndexError:
            print("Can't delete, no row selected.")

    def clear_data(self):
        for child in self.tree.get_children():
            self.tree.delete(child)


if __name__ == "__main__":
    app = StakeholderManager(tk.Tk(), ["Name", "Email"])
    app.root.mainloop()
