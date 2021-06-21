import tkinter as tk
import tkinter.ttk as ttk
import re

from file_messer import *

# Taken from: https://www.askpython.com/python-modules/tkinter/tkinter-treeview-widget
# Modified by Jay Zhong to work with the bioreactor monitoring system.

class StakeholderManager(tk.Frame):
    """ Manages the front and backend aspects of the Stakeholders Settings page.
    """
    def __init__(self, root, controller, colnames):
        """ Initialises StakeholderManager

        :param root: the parent of this widget.
        :param colnames: a list of Strings that determines each column heading.
        """
        tk.Frame.__init__(self, root)
        self.received_data = None
        self.file_directory = os.path.join("assets", "settings", "stakeholders.csv")
        self.id = 0
        self.iid = 0
        self.root = root
        self.controller = controller
        self.initialize_user_interface(colnames)

    def initialize_user_interface(self, colnames):
        """ Creates the frontend "spreadsheet" that the end-user will see and use.
        :param colnames: a list of Strings that determines each column heading.
        """
        # Configure the root object for the Application
        # self.root.title("Stakeholder Manager")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # self.root.config(background="green")

        # Set the treeview
        self.tree = ttk.Treeview(self.root, columns=colnames)
        #self.tree.bind('<ButtonRelease-1>', self.selectName)
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
        """ Inserts a new row of data in the shape of [Name, Email].
        It does so by consecutively asking the user for a name, then a valid email address.
        Details won't be added unless both are valid.
        """
        name = tk.simpledialog.askstring(title="Add Stakeholder",
                                         prompt="Name:")
        if name:
            email = tk.simpledialog.askstring(title="Add Stakeholder",
                                              prompt="Email:")
            if validate_email(email):
                with open(self.file_directory, "a") as stakeholders:
                    stakeholders.write(f"{name},{email}\n")
                self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                     values=(name, email))
                self.iid = self.iid + 1
                self.id = self.id + 1
                self.controller.live_data_manager.mail_bot.add_stakeholder(name, email)
            else:
                tk.messagebox.showinfo(title="Invalid Email", message="Please insert a proper email!")
        else:
            tk.messagebox.showinfo(title="Invalid Name", message="Please insert your name!")

    def insert_data_from_csv(self):
        """ Reads a .csv file to display its data on the frontend "spreadsheet".
        """
        cleanse(self.file_directory)
        stakeholders = open(self.file_directory, "r")
        stakeholders.readline()  # Skip header
        for stakeholder in stakeholders:
            name, email = stakeholder.split(",")
            self.treeview.insert('', 'end', iid=self.iid, text=self.id,
                                 values=(name, email))
            self.iid = self.iid + 1
            self.id = self.id + 1
        stakeholders.close()

    def delete_data(self, selection=None):
        """ Deletes a selected row.
        The selected row is erased both at the front and backend. To maintain stability, the row is replaced by a
        question mark, which will be cleansed when the cleanse() function is invoked by addition new rows.
        :param selection: The index of the selected row.
        """
        try:
            if not selection:
                selected_item = self.tree.selection()[0] # get selected item
            else:
                selected_item = selection

            self.controller.live_data_manager.mail_bot.remove_stakeholder(self.tree.item(self.tree.focus(), "values")[0])
            delete_line(self.file_directory, int(selected_item)+1) # Deletes the line in the .csv file
            self.tree.delete(selected_item)

        except IndexError:
            tk.messagebox.showinfo(title="No target", message="Can't delete, no row selected.")

    def selectName(self, i):
        curItem = self.tree.focus()
        return self.tree.item(curItem, "values")[0]

    def clear_data(self):
        """Replaces the current stakeholders.csv file with a blank .csv file with its heading only.
        """
        with open(self.file_directory, "w+") as f:
            f.write("Name,Email\n")
        for child in self.tree.get_children():
            self.tree.delete(child)
        self.controller.live_data_manager.mail_bot.clear_stakeholder()

    def get(self):
        """ Extracts and returns all values contained within self.tree
        :return: a list of lists, where the first element of a child list is the name of the stakeholder, while the
        second element is their respective email.
        """
        # Inspired by: https://stackoverflow.com/questions/23829409/get-data-from-treeview-in-tkinter
        return [list(map(lambda x: x.strip(), self.tree.item(l)['values'])) for l in self.tree.get_children()]


def validate_email(email):
    """ Regex matches input to determine whether it's a valid email or not.
    :param email: the String that we're interested to see if it's a valid email or not.
    :return:
    """
    # Regex pattern taken from: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    return re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email)


if __name__ == "__main__":
    app = StakeholderManager(tk.Tk(), ["Name", "Email"])
    app.insert_data_from_csv()
    d = app.get()
    print(d)
    app.root.mainloop()
