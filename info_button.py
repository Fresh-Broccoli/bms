import tkinter as tk
from onoff import OnOffButton


class InfoButton(tk.Frame):
    """ Custom widget that combines a tk.Label with a tk.Button.
    It's special in the sense that the two widgets are always placed right next to each other since they're both stored
    in an isolated tk.Frame.
    """

    def __init__(self, master, message, position=tk.RIGHT, **button_param):
        """ Initialises InfoButton
        :param master: the owner of this widget.
        :param message: the text message to be displayed in the tk.Label.
        :param button_type: the class of the widget that we want.
        :param position: tk.Direction, determines where we want the two widgets to be clustered together in the same
            frame.
        :param button_param: parameters for button_type in kwargs.
        """
        super().__init__(master)
        self.label = tk.Label(self, text=message)
        self.button = OnOffButton(self, **button_param)
        self.button.pack(side=position, fill=tk.BOTH)
        self.label.pack(side=position, fill=tk.BOTH)

    def get(self):
        """ Gets the mode of the button.
        :return: 0 or 1.
        """
        return self.button.get()

    def set(self, val):
        """ Sets the mode of the button.
        :param val: 0 or 1.
        """
        if isinstance(val, int):
            self.button.update_settings(val)
        elif isinstance(val, str):
            self.button.update_settings(self.button.translate(val))

    def is_changed(self):
        """ Checks to see if this button has been changed after its previous saved state.
        :return: a Boolean.
        """
        return self.button.changed

    def reset(self):
        """ Resets the button to its previously saved state.
        This involves resetting values and colours.
        """
        if self.button.is_changed():
            self.button.reset()


    def confirm(self):
        """ Confirms that changes have been made,
        by setting variable 'changed' to False.
        """
        self.button.changed = False