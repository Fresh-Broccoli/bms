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
        self.value = tk.StringVar(self)
        self.original_value = tk.StringVar(self)
        self.backend_value = tk.IntVar(self)
        self.changed = False
        self.dictionary = None
        self.menu = tk.OptionMenu(self, self.value, *values)

        if default_value:
            self.set(default_value)
            self.confirm()
            #self._set_og(default_value)


        self.title = tk.Label(self, text=title)
        self.menu.pack(side=tk.BOTTOM)
        self.title.pack(side=tk.BOTTOM)
        self.value.trace("w", self.changed_check)


    def get(self):
        """ Returns the selected value from the list of options.
        :return: an Integer representing the selected value.
        """
        return self.value.get()

    def get_val(self):
        return self.backend_value.get()

    def set(self, value):
        self.value.set(value)

    def changed_check(self, *args):
        #print("Current value: ", self.value.get())
        #print("Original value: ", self._get_og())
        if self.value.get() != self._get_og(): # If current value does not equal to original value, there has been a change.
            self.changed = True # Therefore, there has been a change.
        else:
            self.changed = False # If the two values match, then no changes have been made.

    def confirm(self):
        self.original_value.set(self.value.get())
        if self.dictionary:
            self.backend_value.set(self.dictionary[self.get()])
        else:
            self.backend_value.set(self.get())
        self.changed = False

    def is_changed(self):
        return self.changed

    def reset(self):
        if self.changed:
            self.value.set(self._get_og())
            self.changed = False

    def _get_og(self):
        return self.original_value.get()

    def _set_og(self, value):
        self.original_value.set(value)

    def _change(self):
        self.changed = not self.changed

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Tk dropdown example")
    input = {"Ayy":"A","Bee":"B","See":"C"}
    a = DropDownBox(root, "XD", input, "Ayy")
    a.pack()

    root.mainloop()
