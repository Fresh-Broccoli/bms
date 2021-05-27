# Copied from: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# Credits to Sentdex for providing this TKinter template for free.
# Fullscreen implementation: https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/

import matplotlib
import time
import sys
import os

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from two import TwoLiveData
from treeUI import StakeholderManager
from popups import confirm_box
# from onoff import OnOffButton
from info_button import InfoButton
from menu import DropDownBox
from bio_data import SettingsManager
import tkinter as tk

LARGE_FONT = ("Verdana", 12)
small_font = ("Verdana", 6)
LARGE_FONT_BOLD = LARGE_FONT[0] + " bold", 12


# dataGen = TwoLiveData()


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.attributes("-fullscreen", True)
        self.fullScreenState = False

        # self.bind("<F11>", self.toggleFullScreen)
        # self.bind("<Escape>", self.quitFullScreen)

        self.live_data_manager = TwoLiveData()

        # tk.Tk.iconbitmap(self, default="leaf.ico") # Activating this crashes the Pi version.
        tk.Tk.wm_title(self, "Bioreactor Monitoring System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home, DataSettings, StakeholderSettings):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        for t in ["T1", "T2", "T3", "T4", "T5", "T6"]:
            frame = TubeSettings(container, self)
            self.frames[t] = frame
            frame.grid(row=0,column=0,sticky="news")

        print(self.frames)

        self.show_frame(Home)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.attributes("-fullscreen", self.fullScreenState)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.now = time.strftime('%H:%M:%S')

        top = tk.Frame(self, )
        mid = tk.Frame(self, )
        bottom = tk.Frame(self, )

        top.rowconfigure(0, weight=1)
        top.rowconfigure(1, weight=3)
        top.rowconfigure(2, weight=3)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=8)
        top.columnconfigure(2, weight=1)

        for i in range(5):
            bottom.rowconfigure(i, weight=1)
        for i in range(16):
            bottom.columnconfigure(i, weight=1)

        top.grid(row=0, column=0, sticky="news")
        mid.grid(row=2, column=0, sticky="news")
        bottom.grid(row=4, column=0, sticky="news")

        title = tk.Label(top, text="Welcome Back Captain!", font=LARGE_FONT_BOLD)
        title.grid(row=0, column=1, sticky="news")

        self.clock = tk.Label(top, text=self.now, font=LARGE_FONT)
        self.clock.grid(row=0, column=0, sticky="news")

        quit_button = tk.Button(top,
                                text="Quit",
                                fg="white",
                                bg="red",
                                command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))

        quit_button.grid(row=0, column=2, sticky="ne")

        bio_button = tk.Button(bottom,
                               text="Data Settings",
                               fg="white",
                               bg="black",
                               command=lambda: controller.show_frame(DataSettings))

        bio_button.grid(row=1, column=12, rowspan=3, columnspan=1, sticky="news")

        stake_button = tk.Button(bottom,
                                 text="Stakeholder Settings",
                                 fg="white",
                                 bg="black",
                                 command=lambda: controller.show_frame(StakeholderSettings))

        stake_button.grid(row=1, column=14, rowspan=3, columnspan=1, sticky="news")

        tubes = self.tube_button_maker(bottom)

        # Can't add unique commands in a for-loop for some reason...
        tubes[0]["command"] = lambda: controller.show_frame("T1")
        tubes[1]["command"] = lambda: controller.show_frame("T2")
        tubes[2]["command"] = lambda: controller.show_frame("T3")
        tubes[3]["command"] = lambda: controller.show_frame("T4")
        tubes[4]["command"] = lambda: controller.show_frame("T5")
        tubes[5]["command"] = lambda: controller.show_frame("T6")

        f = controller.live_data_manager.fig
        canvas = FigureCanvasTkAgg(f, mid)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def tube_button_maker(self, parent, buttons=6):
        out = []

        for i in range(1, buttons+1):
            out.append(
                tk.Button(
                    parent,
                    text=f"Tube {i}",
                    fg="white",
                    bg="green",
                    #command= lambda: controller.show_frame(f"T{i}")

                )
            )

            out[-1].grid(row=2, column=i, sticky="ns")

        return out

    def __repr__(self):
        return "Home"


class JsonInteractor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.manager = SettingsManager()

    def _check_changes(self):
        for key, widget in self.widgets.items():
            if widget.is_changed():
                self.manager.changed = True
                break

    def update_settings(self):
        for key, widget in self.widgets.items():
            widget.confirm()
            self.manager.update(key, widget.get())

    def reset(self):
        if self.manager.is_changed():
            for _, widget in self.widgets.items():
                widget.reset()

    def return_home(self, mode="reset"):
        if mode == "reset":
            self._check_changes()
            self.reset()
        elif mode == "confirm":
            self.update_settings()
            self.manager.save()
            confirm_box(restart, "Changed settings will require the program to be restarted in order to take effect. Want to restart now?")
        self.controller.show_frame(Home)


class DataSettings(JsonInteractor):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.widgets = {}
        self.manager = SettingsManager(key="data")

        top = tk.Frame(self,
                       bg="red",
                       )
        bottom = tk.Frame(self,
                          bg="blue",
                          )

        top.grid(row=0, column=0, sticky="nesw")
        bottom.grid(row=1, column=0, sticky="nesw")

        for i in range(3):
            if i != 1:
                top.columnconfigure(i, weight=1)
                bottom.columnconfigure(i, weight=1)
            else:
                top.columnconfigure(i, weight=3)
                bottom.columnconfigure(i, weight=3)

        for i in range(5):
            top.rowconfigure(i, weight=1)
            bottom.rowconfigure(i, weight=1)


        data_setting_menu = tk.Frame(top,
                                     bg="#8bf773",
                                     )
        data_setting_menu.grid(row=1,
                               column=1,
                               rowspan=3,
                               sticky="news",
                               )

        data_setting_menu.rowconfigure(0, weight=1)
        data_setting_menu.rowconfigure(1, weight=3)
        data_setting_menu.rowconfigure(2, weight=3)
        data_setting_menu.columnconfigure(0, weight=1)
        data_setting_menu.columnconfigure(1, weight=1)

        label = tk.Label(top, text="Data Settings", font=LARGE_FONT_BOLD)
        label.grid(row=0,
                   column=1,
                   sticky="n",
                   # padx=5,
                   # pady=5,
                   )

        data_title = tk.Label(data_setting_menu,
                              text="Data Settings",
                              font=LARGE_FONT
                              )

        data_title.grid(row=0,
                        column=0,
                        columnspan=2)

        home_button = tk.Button(top,
                                text="Back to Home",
                                fg="white",
                                bg="green",
                                command=lambda: confirm_box(self.return_home, "Unsaved changes will be rolled back.\n "
                                                                              "Are you sure?"))

        home_button.grid(row=0,
                         column=0,
                         sticky="nw",
                         # padx=5,
                         # pady=5
                         )


        data_points = DropDownBox(data_setting_menu,
                                  "No. of data points: ",
                                  [i for i in range(3, 16)],
                                  self.manager.get()["data_points"]
                                  )
        data_points.grid(row=1,
                         column=0,
                         )

        self.widgets["data_points"] = data_points

        read_interval = DropDownBox(data_setting_menu, "Read Interval: ",
                                    [
                                        "1sec",
                                        "5sec",
                                        "10sec",
                                        "15sec",
                                        "30sec",
                                        "1min",
                                        "5min",
                                        "10min",
                                        "30min",
                                        "1hour",
                                        "3hour",
                                        "6hour",
                                        "12hour",
                                        "24hour"
                                    ],
                                    self.manager.get()["read_interval"])
        read_interval.grid(row=1,
                           column=1,
                           )

        self.widgets["read_interval"] = read_interval

        data_life = DropDownBox(data_setting_menu, "Data Lifespan: ",
                                [
                                    "1day",
                                    "2day",
                                    "3day",
                                    "4day",
                                    "5day",
                                    "6day",
                                    "1week",
                                    "2week",
                                    "3week",
                                    "1mon",
                                    "2mon",
                                    "3mon",
                                    "4mon"
                                ],
                                self.manager.get()["data_life"]
                                )

        data_life.grid(row=1,
                       column=0,
                       columnspan=2
                       )

        self.widgets["data_life"] = data_life

        confirm = tk.Button(bottom,
                            text="Confirm",
                            command=lambda: confirm_box(self.return_home, "Are you sure you want to save your changes?",
                                                        "confirm"),
                            fg="white",
                            bg="red",
                            height=5,
                            width=20
                            )
        confirm.grid(row=4,
                     column=1,
                     # sticky="news",
                     )
    def __repr__(self):
        return "DataSettings"

class TubeSettings(JsonInteractor):
    no = 0
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        TubeSettings.no += 1
        self.no = TubeSettings.no
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.widgets = {}
        self.manager = SettingsManager(f"tube{self.no}")

        top = tk.Frame(self,
                       bg="red",
                       )
        bottom = tk.Frame(self,
                          bg="blue",
                          )

        top.grid(row=0, column=0, sticky="nesw")
        bottom.grid(row=1, column=0, sticky="nesw")

        for i in range(3):
            if i != 1:
                top.columnconfigure(i, weight=1)
                bottom.columnconfigure(i, weight=1)
            else:
                top.columnconfigure(i, weight=3)
                bottom.columnconfigure(i, weight=3)

        for i in range(5):
            top.rowconfigure(i, weight=1)
            bottom.rowconfigure(i, weight=1)

        bio_setting_menu = tk.Frame(top,
                                    bg="#daf542"
                                    )
        bio_setting_menu.grid(row=1,
                              column=1,
                              rowspan=3,
                              sticky="news"
                              )

        bio_setting_menu.rowconfigure(0, weight=1)
        bio_setting_menu.rowconfigure(1, weight=3)
        bio_setting_menu.rowconfigure(2, weight=3)
        bio_setting_menu.columnconfigure(0, weight=1)
        bio_setting_menu.columnconfigure(1, weight=1)

        data_setting_menu = tk.Frame(bottom,
                                     bg="#8bf773",
                                     )
        data_setting_menu.grid(row=0,
                               column=1,
                               rowspan=3,
                               sticky="news",
                               )

        label = tk.Label(top, text=f"Tube {self.no} Settings", font=LARGE_FONT_BOLD)
        label.grid(row=0,
                   column=1,
                   sticky="n",
                   # padx=5,
                   # pady=5,
                   )

        home_button = tk.Button(top,
                                text="Back to Home",
                                fg="white",
                                bg="green",
                                command=lambda: confirm_box(self.return_home, "Unsaved changes will be rolled back.\n "
                                                                              "Are you sure?"))

        home_button.grid(row=0,
                         column=0,
                         sticky="nw",
                         # padx=5,
                         # pady=5
                         )

        bio_setting_menu.columnconfigure(0, weight=1)
        bio_setting_menu.rowconfigure(0, weight=1)
        bio_setting_menu.rowconfigure(1, weight=3)
        bio_setting_menu.rowconfigure(2, weight=3)

        bio_title = tk.Label(bio_setting_menu, text="Tube Settings", font=LARGE_FONT)
        bio_title.grid(row=0,
                       column=0,
                       columnspan=2
                       )

        heater = InfoButton(master=bio_setting_menu,
                            message="Heaters: ",
                            text=self.manager.get()["heater"])
        heater.grid(row=1,
                    column=0,
                    # sticky="news",
                    )

        self.widgets["heater"] = heater

        air = InfoButton(master=bio_setting_menu,
                         message="Air Pumps: ",
                         text=self.manager.get()["air"]
                         )

        air.grid(row=2,
                 column=0,
                 # sticky="news"
                 )
        self.widgets["air"] = air

        light = InfoButton(master=bio_setting_menu,
                           message="Lights: ",
                           text=self.manager.get()["light"]
                           )
        light.grid(row=1,
                   column=1,
                   # sticky="news"
                   )
        self.widgets["light"] = light

        food = InfoButton(master=bio_setting_menu,
                          message="Food Pumps: ",
                          text=self.manager.get()["food"]
                          )
        food.grid(row=2,
                  column=1,
                  # sticky="news"
                  )
        self.widgets["food"] = food

        confirm = tk.Button(bottom,
                            text="Confirm",
                            command=lambda: confirm_box(self.return_home, "Are you sure you want to save your changes?",
                                                        "confirm"),
                            fg="white",
                            bg="red",
                            height=5,
                            width=20
                            )
        confirm.grid(row=4,
                     column=1,
                     # sticky="news",
                     )



    def __repr__(self):
        return "Tube " + str(self.no)

class StakeholderSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        top = tk.Frame(self, bg="red")
        top.grid(row=0, column=0, sticky="news")
        mid = tk.Frame(self, bg="yellow")
        mid.grid(row=1, column=0, sticky='news')
        bottom = tk.Frame(self, bg="blue")
        bottom.grid(row=2, column=0, sticky="nwes")

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)

        bottom.rowconfigure(0, weight=1)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.columnconfigure(2, weight=1)

        title = tk.Label(top, text="Stakeholder Settings", font=LARGE_FONT_BOLD)
        title.grid(row=0, column=1, sticky="n")

        home_button = tk.Button(
            top,
            text="Back to Home",
            fg="white",
            bg="green",
            command=lambda: controller.show_frame(Home)
        )

        home_button.grid(row=0,
                         column=0,
                         sticky="nw",
                         # padx=5,
                         # pady=5,
                         )

        table = StakeholderManager(mid, ["Name", "Email"])
        table.insert_data_from_csv()

        add = tk.Button(
            bottom,
            text="Add Stakeholder",
            font=("bold", 20),
            bg="green",
            command=table.insert_data
        )

        add.grid(row=0,
                 column=0,
                 sticky="news",
                 # padx=15,
                 # pady=15,
                 )

        delete = tk.Button(
            bottom,
            text="Delete Stakeholder",
            font=("bold", 20),
            bg="red",
            command=lambda: confirm_box(table.delete_data, "Are you sure you want to delete this stakeholder?"),
        )

        delete.grid(row=0,
                    column=1,
                    sticky="news",
                    # padx=15,
                    # pady=15,
                    )

        clear = tk.Button(
            bottom,
            text="Clear Stakeholders",
            font=("bold", 20),
            bg="white",
            command=lambda: confirm_box(table.clear_data, "Are you sure you want to clear all data?")
        )

        clear.grid(row=0,
                   column=2,
                   sticky="news",
                   # padx=15,
                   # pady=15,
                   )

    def _repr__(self):
        return "StakeholderSettings"


class UserInteractor:
    """ Class used for creating widgets that allow user-interaction.
    This class was created to store a name that will be used to identify collected data.
    """

    def __init__(self, name, type, *args, **settings):
        self.name = name
        self.widget = type(*args, **settings)

    def get(self):
        return self.widget.get()

    def pack(self, *args, **kwargs):
        self.widget.pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        # print(args, kwargs)
        self.widget.place(*args, **kwargs)

    def grid(self, *args, **kwargs):
        # print(args, kwargs)
        self.widget.grid(*args, **kwargs)


def get_parameters(page):
    """ Gets values of widgets from a specific page.
    Said page MUST contain a dictionary named 'self.widgets' for this to work.
    Parameter
    ---------
    page (tk.Frame *custom): a custom tk.Frame object containing self.widgets.

    Return
    ------
    A dictionary with the name of the widget as the key, and its value as the element.

    """
    out = {}
    for typ, dic in page.widgets.items():
        temp_dict = {}
        for name, widget in dic.items():
            temp_dict[name] = widget.get()
        out[typ] = temp_dict
    return out


def print_output(func, *args):
    print(func(*args))


# Time and tick are copied from:
# https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python
def tick(page, tick_rate=1000):
    now = time.strftime("%H:%M:%S")
    if page.now != now:
        page.now = now
        page.clock.config(text=now)
    page.clock.after(tick_rate, lambda: tick(page, tick_rate))

def restart():
    """ Restarts the entire program.
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    app = Application() # Runs the UI.
    tick(app.frames[Home]) # Allows the clock to run.
    ani = app.live_data_manager.animator(1000) # Allows data visualisation.
    app.mainloop()
