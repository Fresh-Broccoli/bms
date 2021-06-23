import tkinter as tk

class OnOffButton(tk.Button):
    """ Custom button widget that can change its colour and text.
    """
    mode = {"On":(1, "green"), "Off":(0, "red")}

    def __init__(self, master, text="On", on_command=None, off_command=None):
        """ Constructor
        Initialises the button widget by setting it 'On' by default.
        :param master: the owner of this widget.
        :param text: What to display as button text.
        """
        super().__init__(master)
        self["text"] = text
        self["command"] = self.switch
        self["fg"] = "white"
        self.changed = False
        self.update_settings(text)
        self.on_command = on_command
        self.off_command = off_command

    def switch(self):
        """ Flips the switch
        If the button is on, turn it off. If the button is off, turn it on.
        """
        self._change()
        if self.value:
            self.update_settings("Off")
            if (self.off_command is not None):
                self.off_command()
        else:
            self.update_settings("On")
            if (self.on_command is not None):
                self.on_command()

    def get(self):
        """ Gets the value stored in a button. Either "On" or "Off"
        :return: A String
        """
        return self.translate(self.value)

    def set(self, mode):
        """ Forces OnOffButton to switch on/off depending on mode
        :param mode: 0 or 1
        """
        if self.value:
            if self.value != mode:
                self.switch()
        else:
            raise ValueError

    def update_settings(self, text):
        """ Change button attributes to reflect on the flip of the switch.
        Changing the mode of the button will change attributes associated with said mode. These include:
            - Button colour
            - Button text
            - Button value (mode)
        :param text: Either "On" or "Off"
        """
        self.settings = OnOffButton.mode[text]
        self.value = self.settings[0]
        self.config(text=text)
        self["bg"] = self.settings[1]

    def translate(self, num):
        """ Converts binary values to Strings that determine the mode of the button.
        0 is converted to "Off", while 1 is converted to "On".
        :param num: Either 0 or 1. Can also be "On" or "Off".
        :return: "On" or "Off" depending on the input parameter 'num'.
        """
        if num == 0:
            return "Off"
        elif num == 1:
            return "On"
        else:
            if num == "On" or num == "Off":
                return num
            raise ValueError

    def is_changed(self):
        """ Checks if the button has been clicked after the state where its changes were saved.
        :return: a Boolean.
        """
        return self.changed

    def reset(self):
        """ Resets the button to its previously saved state.
        This involves resetting values and colours.
        """
        if self.changed:
            self.switch()

    def _change(self, *args):
        """
        Reverses self.changed after the on/off button is pressed. This will guarantee that if the button is pressed
        twice (eg: on > off > on), it will remain unchanged.
        :param args: Needed for the trace function to work.
        :return:
        """
        self.changed = not self.changed
        #print(self.changed)

if __name__ == "__maine__":

    # Create an instance of window of frame
    win = tk.Tk()

    # set Title
    win.title('On/Off Demonstration')

    # Set the Geometry
    win.geometry("600x400")
    win.resizable(0,0)

    #on_dir = os.path.join("assets", "images", "on.png")
    #off_dir = os.path.join("assets", "images", "off.png")

    #Create a variable to turn on the button initially

    # Create Label to display the message
    label = tk.Label(win,text = "Night Mode is On",bg= "white",fg ="black",font =("Poppins bold", 22))
    label.pack(pady = 20)

    # Define Our Images

    # Create A Button
    on= OnOffButton(win)
    on.pack(pady = 50)

    #Keep Running the window
    win.mainloop()
