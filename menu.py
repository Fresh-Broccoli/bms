import tkinter as tk

class DropDownBox(tk.Frame):
    """ Custom OptionMenu stored within a tk.Frame.
    """
    def __init__(self, master, title, values, default_value=None):
        """ Initialises DropDownBox
        :param master: The owner of this frame.
        :param title: The text above the OptionMenu box.
        :param default_value: The default value shown by the OptionMenu box. Useful for loading predetermined values.
        :param values: A list/dictionary of options that the user can choose from. It excludes the option from default_value.
        """
        super().__init__(master)
        self.value = tk.IntVar(self)

        if default_value:
            self.value.set(default_value)

        if isinstance(values, dict):
            self.dictionary = values
            self.menu = tk.OptionMenu(self, self.value, *values.keys())
        else:
            self.menu = tk.OptionMenu(self, self.value, *values)
        self.title = tk.Label(self, text=title)
        self.menu.pack(side=tk.BOTTOM)
        self.title.pack(side=tk.BOTTOM)

    def get(self):
        """ Returns the selected value from the list of options.
        :return: The selected value.
        """
        return self.dictionary[self.value.get()] if self.dictionary else self.value.get()

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Tk dropdown example")
    input = {"Ayy":"A","Bee":"B","See":"C"}
    a = DropDownBox(root, "XD", input, "Ayy")
    a.pack()

    root.mainloop()
