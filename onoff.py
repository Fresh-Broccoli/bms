import tkinter as tk

class OnOffButton(tk.Button):
    """ Custom button widget that can change its colour and text.
    """
    mode = {"On":(1, "green"), "Off":(0, "red")}

    def __init__(self, master, text="On"):
        """ Constructor
        Initialises the button widget by setting it 'On' by default.
        :param master: the owner of this widget.
        :param text: What to display as button text.
        """
        super().__init__(master)
        self["text"] = text
        self["command"] = self.switch
        self["fg"] = "white"
        self.update_settings(text)

    def switch(self):
        """ Flips the switch
        If the button is on, turn it off. If the button is off, turn it on.
        """
        if self.mode:
            self.update_settings("Off")

        else:
            self.update_settings("On")


    def update_settings(self, text):
        """ Change button attributes to reflect on the flip of the switch.
        Changing the mode of the button will change attributes associated with said mode. These include:
            - Button colour
            - Button text
            - Button value (mode)
        :param text: Either "On" or "Off"
        """
        self.settings = OnOffButton.mode[text]
        self.mode = self.settings[0]
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