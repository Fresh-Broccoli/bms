import tkinter as tk
import tkinter.ttk as ttk


# Taken from: https://www.askpython.com/python-modules/tkinter/tkinter-treeview-widget
# Modified by Jay Zhong to work with the bioreactor monitoring system.

class StakeholderManager(tk.Frame):
    def __init__(self, root, colnames):
        tk.Frame.__init__(self, root)
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

        """
        # Define the different GUI widgets
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_entry = tk.Entry(self.root)
        self.name_label.grid(row=0, column=0, sticky=tk.W)
        self.name_entry.grid(row=0, column=1)

        self.idnumber_label = tk.Label(self.root, text="ID")
        self.idnumber_entry = tk.Entry(self.root)
        self.idnumber_label.grid(row=1, column=0, sticky=tk.W)
        self.idnumber_entry.grid(row=1, column=1)

        self.submit_button = tk.Button(self.root, text="Insert", command=self.insert_data)
        self.submit_button.grid(row=2, column=1, sticky=tk.W)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=0, column=3)
        """

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

    def insert_data(self, *data):
        self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                             values=data)
        self.iid = self.iid + 1
        self.id = self.id + 1

    def delete_data_master(self):
        id = tk.simpledialog.askstring(title="Delete Stakeholder",
                                       prompt="Insert Stakeholder ID: ")
        self.delete_data(id)

    def delete_data(self, iid):
        self.treeview.delete(iid)

    def clear_data(self):
        for i in range(self.iid):
            self.delete_data(i)
        self.id, self.iid = 0, 0

if __name__ == "__main__":
    app = StakeholderManager(tk.Tk(), ["Name", "Email"])
    app.root.mainloop()
